"""Moore FSM Bus Functional Model (BFM).

Provides the cocotb interface to the Moore state machine DUT.
Manages stimulus application and response monitoring for the Moore FSM.

Operational Flow:
- Driver sends transactions to driver_queue
- Driver task applies inputs (next_i, rst_i) to DUT
- Monitor task captures state transitions and outputs after clock edge
- Results returned via mon_queue

Moore Machine Interface:
- Inputs: clk_i, next_i, rst_i
- Output: out_o
- State: state_moore (internal state register)
"""

from cocotb.triggers import Timer, Event, RisingEdge, FallingEdge
import cocotb
from cocotb.queue import Queue
from cocotb.clock import Clock

class MooreWrapper:
    """Bus Functional Model wrapper for Moore FSM DUT.
    
    Manages:
        - Clock generation (10 ns period)
        - Input stimulus application
        - Output and state monitoring
        - Synchronization between driver and monitor
    
    Uses queues and events for proper sequencing of transactions.
    """
    def __init__(self):
        """Initialize Moore FSM BFM.
        
        Sets up:
            - DUT reference (cocotb.top)
            - Driver and monitor queues
            - Synchronization events
            - Previous state tracking
        """
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 
        self.previous_state=0

    async def send_pkt(self, packet):
        """Send transaction packet to driver queue.
        
        Args:
            packet: Pkt object with next_i and rst_i values
        
        Waits for acknowledgment before queuing new packet.
        """
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        """Driver coroutine - applies inputs to Moore FSM.
        
        Continuously:
            - Gets packet from driver_queue
            - Applies next_i and rst_i to DUT
            - Captures previous state
            - Signals monitor that stimulus is ready
        """
        while True:
            packet = await self.driver_queue.get() 
            
            self.dut.next_i.value = packet.next_i
            self.dut.rst_i.value = packet.rst_i
            self.previous_state=self.dut.state_moore.value
            self.stimulus_event.set()

    async def get_result(self):
        """Retrieve monitored result from queue.
        
        Returns:
            Tuple: (next_i, rst_i, out_o, previous_state, current_state)
        """
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        """Monitor coroutine - captures Moore FSM outputs and states.
        
        Continuously:
            - Waits for stimulus event
            - Samples DUT after rising clock edge
            - Captures inputs, output, and state transition
            - Sends results to monitor queue
            - Acknowledges completion
        """
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            await RisingEdge(self.dut.clk_i)
            await Timer(1, unit='ps')
            
            NEXT_i = self.dut.next_i.value
            RST_i = self.dut.rst_i.value
            OUT_o = self.dut.out_o.value
            PREVIOUS_STATE_x = self.previous_state
            CURRENT_STATE_x = self.dut.state_moore.value

            self.mon_queue.put_nowait((NEXT_i, RST_i, OUT_o, PREVIOUS_STATE_x, CURRENT_STATE_x))
            
            self.ack_event.set()
            
    def start_bfm(self):
        """Start the Bus Functional Model.
        
        Launches:
            - Clock generator (10 ns period)
            - Driver task coroutine
            - Monitor task coroutine
        
        Called during build phase to initialize BFM operation.
        """
        c = Clock(self.dut.clk_i, 10, unit="ns")
        cocotb.start_soon(c.start())
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())