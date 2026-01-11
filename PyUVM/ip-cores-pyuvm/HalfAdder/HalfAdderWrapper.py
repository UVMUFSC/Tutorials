from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class HalfAdderWrapper:
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
            
            self.dut.a.value = packet.a
            self.dut.b.value = packet.b 
            self.stimulus_event.set()

    async def get_result(self):
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        ##await Timer(1, unit='step')
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
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())