"""DemuxWrapper: Bus Functional Model (BFM) for 1x4 Demux DUT.

Low-level interface that directly drives and monitors DUT signals via cocotb.
Decouples the UVM testbench from raw Verilog signal manipulation by providing
async driver and monitor tasks that translate packets into DUT operations.

Signal mapping:
- Inputs (from driver): x_i (1-bit data), sel_i (2-bit selector)
- Outputs (monitored): y0_o, y1_o, y2_o, y3_o (4 output lines)
"""

from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class DemuxWrapper:
    """Bus Functional Model for 1x4 demultiplexer.
    
    Provides async driver_task (DUT input actuation) and monitor_task (DUT output
    observation) that coordinate via internal queues. Routes single x_i input to
    one of 4 outputs based on sel_i selector value.
    """

    def __init__(self):
        """Initialize BFM: Set up DUT reference, queues, and synchronization events.
        
        - driver_queue: Accepts packets from UVM driver (maxsize=1 for backpressure)
        - mon_queue: Delivers monitored results to UVM monitor (maxsize=0 = unbuffered)
        - ack_event: Handshake signal (driver waits for completion before next packet)
        - stimulus_event: Synchronizes driver and monitor tasks
        """
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 

    async def send_pkt(self, packet):
        """Driver interface: Accepts a packet and queues it for DUT actuation.
        
        Handshake:
        1. Wait for ack_event (previous packet completed)
        2. Clear ack_event (indicate driver is busy)
        3. Put packet on driver_queue for driver_task to consume
        """
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        """Continuous task: Actuate DUT inputs from queued packets.
        
        For each packet:
        1. Wait for packet from driver_queue
        2. Assign DUT input signals (x_i, sel_i)
        3. Set stimulus_event to trigger monitor observation
        """
        while True:
            packet = await self.driver_queue.get() 
            
            self.dut.x_i.value = packet.x_i
            self.dut.sel_i.value = packet.sel_i
            self.stimulus_event.set()

    async def get_result(self):
        """Monitor interface: Retrieve next observed DUT result.
        Blocks until monitor_task publishes a result on mon_queue.
        """
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        """Continuous task: Observe DUT outputs and publish results.
        
        For each stimulus:
        1. Wait for stimulus_event (driver has applied inputs)
        2. Clear stimulus_event (indicate monitor is busy)
        3. Sample DUT output signals (y0_o, y1_o, y2_o, y3_o)
        4. Also capture inputs (x_i, sel_i) for correlation
        5. Queue result tuple to mon_queue for monitor to retrieve
        6. Set ack_event to allow driver to apply next packet
        """
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            
            Y0_o = self.dut.y0_o.value
            Y1_o = self.dut.y1_o.value
            Y2_o = self.dut.y2_o.value
            Y3_o = self.dut.y3_o.value
            X_i = self.dut.x_i.value
            SEL_i = self.dut.sel_i.value
            
            self.mon_queue.put_nowait((X_i, SEL_i, Y0_o, Y1_o, Y2_o, Y3_o))
            
            self.ack_event.set()
            
    def start_bfm(self):
        """Start BFM: Launch driver and monitor tasks as concurrent cocotb coroutines.
        Called during testbench initialization to enable signal-level simulation.
        """
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())