from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class FullAdderWrapper:
    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 

    async def send_pkt(self, packet):
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        while True:
            packet = await self.driver_queue.get() 
            
            self.dut.a_i.value = packet.a_i
            self.dut.b_i.value = packet.b_i 
            self.dut.carry_i.value = packet.carry_i 
            self.stimulus_event.set()

    async def get_result(self):
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        ##await Timer(1, unit='step')
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
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())