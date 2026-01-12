from cocotb.triggers import Timer, Event, RisingEdge, FallingEdge
import cocotb
from cocotb.queue import Queue
from cocotb.clock import Clock

class MooreWrapper:
    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 
        self.previous_state=0

    async def send_pkt(self, packet):
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        while True:
            packet = await self.driver_queue.get() 
            
            self.dut.next_i.value = packet.next_i
            self.dut.rst_i.value = packet.rst_i
            self.previous_state=self.dut.state_moore.value
            self.stimulus_event.set()

    async def get_result(self):
        return await self.mon_queue.get()
    
    async def monitor_task(self):
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
        c = Clock(self.dut.clk_i, 10, unit="ns")
        cocotb.start_soon(c.start())
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())