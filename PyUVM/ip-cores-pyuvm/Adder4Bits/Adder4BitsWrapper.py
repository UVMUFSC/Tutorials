"""
Adder4BitsWrapper: Bus Functional Model (BFM) for 4-bit Adder DUT.

Provides the low-level interface between Python testbench and Verilog DUT.
Handles cocotb signal manipulation, clock generation, and handshaking.
Essentially acts as an adapter between the synchronous RTL world and async Python world.
"""

from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class Adder4BitsWrapper:
    """
    BFM: bridges testbench and DUT communication.
    
    Operation:
    - driver_task: drives input signals to DUT
    - monitor_task: observes DUT outputs
    - Coordinates handshaking to ensure proper timing
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
        Send a packet to the DUT.
        
        Called by driver: waits for acknowledgment, then queues the packet
        for the driver_task to apply to DUT signals.
        """
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        """
        Driver background task: apply packets to DUT inputs.
        
        Continuously waits for packets from the driver, applies their values
        to the DUT input signals, and signals the monitor that new stimulus is ready.
        """
        while True:
            packet = await self.driver_queue.get() 
            self.dut.a_i.value = packet.a_i
            self.dut.b_i.value = packet.b_i 
            self.stimulus_event.set()

    async def get_result(self):
        """Retrieve result tuple from DUT (called by monitor)."""
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        """
        Monitor background task: observe and capture DUT outputs.
        
        Waits for stimulus event, reads all DUT outputs, packages them,
        and queues for the monitor component to retrieve.
        """
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            A_in = self.dut.a_i.value
            B_in = self.dut.b_i.value
            C_out = self.dut.c_o.value
            S_out = self.dut.s_o.value
            self.mon_queue.put_nowait((A_in, B_in, C_out, S_out))
            self.ack_event.set()
    
    def start_bfm(self):
        """Start driver and monitor background tasks."""
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())