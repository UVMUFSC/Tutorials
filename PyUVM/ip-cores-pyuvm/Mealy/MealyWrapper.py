from cocotb.triggers import Timer, Event, RisingEdge, FallingEdge
import cocotb
from cocotb.queue import Queue
from cocotb.clock import Clock

class MealyWrapper:
    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 
        self.current_state=0

    async def send_pkt(self, packet):
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        while True:
            packet = await self.driver_queue.get() 

            self.current_state=self.dut.state.value
            self.dut.mealy_i.value = packet.mealy_i
            self.dut.rst_i.value = packet.rst_i
            
            self.stimulus_event.set()

    async def get_result(self):
        return await self.mon_queue.get()
    
    async def monitor_task(self):
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
        c = Clock(self.dut.clk_i, 10, unit="ns")
        cocotb.start_soon(c.start())
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())