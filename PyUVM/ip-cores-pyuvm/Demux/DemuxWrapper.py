from cocotb.triggers import Timer, Event
import cocotb
from cocotb.queue import Queue

class DemuxWrapper:
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
            
            self.dut.x_i.value = packet.x_i
            self.dut.sel_i.value = packet.sel_i
            self.stimulus_event.set()

    async def get_result(self):
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        ##await Timer(1, unit='step')
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
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())