"""
Mealy Machine Verification - Bus Functional Model (BFM)

Provides cocotb interface layer for Mealy FSM DUT.
Handles clock generation, driver task, and monitor task.

Key features:
- Synchronous driver: applies inputs on clock edge
- Monitor: captures outputs (combinational based on state + input)
- State tracking: records current_state before transitions
"""

from cocotb.triggers import Timer, Event, RisingEdge, FallingEdge
import cocotb
from cocotb.queue import Queue
from cocotb.clock import Clock

class MealyWrapper:
    """
    Bus Functional Model for Mealy FSM
    
    Manages communication between PyUVM components and cocotb DUT:
    - Driver queue: receives packets from driver
    - Monitor queue: sends captured results to monitor
    - Event synchronization: coordinates driver/monitor activity
    - State tracking: captures current_state before transitions
    """
    def __init__(self):
        """
        Initialize BFM with queues, events, and DUT reference.
        """
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 
        self.current_state=0

    async def send_pkt(self, packet):
        """
        Send packet from driver to BFM driver task.
        
        Args:
            packet: Transaction item containing mealy_i, rst_i
        """
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        """
        Driver coroutine: apply inputs to DUT.
        
        Workflow:
        1. Get packet from driver queue
        2. Capture current state before inputs change
        3. Apply mealy_i and rst_i to DUT
        4. Signal monitor to capture outputs
        """
        while True:
            packet = await self.driver_queue.get() 

            self.current_state=self.dut.state.value
            self.dut.mealy_i.value = packet.mealy_i
            self.dut.rst_i.value = packet.rst_i
            
            self.stimulus_event.set()

    async def get_result(self):
        """
        Retrieve monitored result (called by monitor).
        
        Returns:
            Tuple: (mealy_i, rst_i, mealy_o, next_state, current_state)
        """
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        """
        Monitor coroutine: capture DUT outputs and states.
        
        Workflow:
        1. Wait for stimulus event (inputs applied)
        2. Capture combinational output (mealy_o)
        3. Wait for clock edge (state transition)
        4. Capture next_state after clock
        5. Put result tuple in monitor queue
        6. Signal acknowledgment for next transaction
        """
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            await Timer(1, unit='ns')
            self.NEXT_STATE_x = self.dut.next_state.value
            self.MEALY_o = self.dut.mealy_o.value 
            self.MEALY_i = self.dut.mealy_i.value
            self.RST_i = self.dut.rst_i.value
            self.CURRENT_STATE_x = self.current_state
            await RisingEdge(self.dut.clk_i)
            await Timer(1, unit='ps')

            if(self.dut.rst_i.value == 0):
                self.NEXT_STATE_x = self.dut.state.value

            self.mon_queue.put_nowait((self.MEALY_i, self.RST_i, self.MEALY_o, self.NEXT_STATE_x, self.CURRENT_STATE_x))
            
            self.ack_event.set()
            
    def start_bfm(self):
        """
        Start BFM coroutines and clock generation.
        
        Launches:
        - Clock generator (10ns period)
        - Driver task
        - Monitor task
        """
        c = Clock(self.dut.clk_i, 10, unit="ns")
        cocotb.start_soon(c.start())
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())