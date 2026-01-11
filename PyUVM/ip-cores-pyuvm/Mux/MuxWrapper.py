from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class MuxWrapper:
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
            
            self.dut.x0_i.value = packet.x0_i
            self.dut.x1_i.value = packet.x1_i
            self.dut.x2_i.value = packet.x2_i
            self.dut.x3_i.value = packet.x3_i
            self.dut.sel_i.value = packet.sel_i
            self.dut.y_o.value = packet.y_o
            self.stimulus_event.set()

    async def get_result(self):
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        ##await Timer(1, unit='step')
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            
            X0_i = self.dut.x0_i.value
            X1_i = self.dut.x1_i.value
            X2_i = self.dut.x2_i.value
            X3_i = self.dut.x3_i.value
            SEL_i = self.dut.sel_i.value
            Y_o = self.dut.y_o.value
            
            self.mon_queue.put_nowait((X0_i, X1_i, X2_i, X3_i, SEL_i, Y_o))
            
            self.ack_event.set()
            
    def start_bfm(self):
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())