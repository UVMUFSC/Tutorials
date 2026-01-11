from pyuvm import *

class MyDriver(uvm_driver):

    def __init__(self, name, parent):
        super().__init__(name, parent)

    def build_phase(self):
        self.bfm = ConfigDB().get(self, "", "BUS_BFM")

    async def run_phase(self):
        while True:
            packet=await self.seq_item_port.get_next_item()
            await self.bfm.send_pkt(packet)
            self.seq_item_port.item_done()
