"""
HalfAdderWrapper: Bus Functional Model (BFM) for Half Adder DUT interface.

Provides driver and monitor tasks to interact with DUT signals:
- Inputs: a_i, b_i
- Outputs: sum_o, carry_o
"""

from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class HalfAdderWrapper:
    """
    BFM wrapper that bridges UVM components to cocotb DUT.
    
    - Driver task: applies packets to DUT inputs
    - Monitor task: captures DUT outputs
    - Synchronizes via queues and events
    """

    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 

    async def send_pkt(self, packet):
        """
        Send packet to driver task (called by MyDriver).
        """
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        """
        Driver coroutine: Apply packet inputs to DUT.
        """
        while True:
            packet = await self.driver_queue.get() 
            
            self.dut.a.value = packet.a
            self.dut.b.value = packet.b 
            self.stimulus_event.set()

    async def get_result(self):
        """
        Fetch monitored result (called by MyMonitor).
        """
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        """
        Monitor coroutine: Capture DUT outputs and queue for monitor.
        """
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            
            A_in = self.dut.a.value
            B_in = self.dut.b.value
            S_out = self.dut.s.value
            C_out = self.dut.c.value
            
            self.mon_queue.put_nowait((A_in, B_in, S_out, C_out))
            
            self.ack_event.set()
            
    def start_bfm(self):
        """
        Launch driver and monitor background tasks.
        """
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())