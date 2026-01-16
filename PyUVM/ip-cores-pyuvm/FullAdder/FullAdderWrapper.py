"""
FullAdderWrapper: Bus Functional Model (BFM) for Full Adder DUT.

Provides the low-level interface between Python testbench and Verilog Full Adder DUT.
Handles cocotb signal manipulation (a_i, b_i, carry_i → sum_o, carry_o), and handshaking.
Essentially acts as an adapter between the synchronous RTL world and async Python world.
"""

from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class FullAdderWrapper:
    """
    BFM: bridges testbench and Full Adder DUT communication.
    
    Operation:
    - driver_task: drives input signals (a_i, b_i, carry_i) to DUT
    - monitor_task: observes DUT outputs (sum_o, carry_o)
    - Coordinates handshaking to ensure proper timing and synchronization
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
        Send a Full Adder packet to the DUT.
        
        Called by driver: waits for acknowledgment, then queues the packet
        for the driver_task to apply to DUT input signals (a_i, b_i, carry_i).
        """
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        """
        Driver background task: apply Full Adder packets to DUT inputs.
        
        Continuously waits for packets from the driver, applies their values
        to the DUT input signals (a_i, b_i, carry_i), and signals monitor that new stimulus is ready.
        """
        while True:
            packet = await self.driver_queue.get() 
            
            self.dut.a_i.value = packet.a_i
            self.dut.b_i.value = packet.b_i 
            self.dut.carry_i.value = packet.carry_i 
            self.stimulus_event.set()

    async def get_result(self):
        """
        Get Full Adder DUT result.
        
        Called by monitor: retrieves sampled DUT signals from monitor_task.
        Returns tuple: (a_i, b_i, carry_i, carry_o, sum_o)
        """
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        """
        Monitor background task: sample Full Adder DUT signals.
        
        Waits for stimulus event, then samples all DUT signals (a_i, b_i, carry_i inputs
        and sum_o, carry_o outputs), queues them for monitor, and signals acknowledgment.
        """
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            
            A_in = self.dut.a_i.value
            B_in = self.dut.b_i.value
            C_in = self.dut.carry_i.value
            S_out = self.dut.sum_o.value
            C_out = self.dut.carry_o.value
            
            self.mon_queue.put_nowait((A_in, B_in, C_in, C_out, S_out))
            
            self.ack_event.set()
            
    def start_bfm(self):
        """
        Start Full Adder BFM background tasks.
        
        Launches driver_task and monitor_task as concurrent coroutines
        to handle DUT signal manipulation and observation.
        """
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())