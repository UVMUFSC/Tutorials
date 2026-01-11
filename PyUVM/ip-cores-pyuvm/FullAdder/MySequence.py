from pyuvm import *
from Pkt import Pkt
from MyCoverage import MyCoverage
from cocotb.triggers import Timer


class MySequence(uvm_sequence):

    def __init__(self, name):
        super().__init__(name)
        self.cov_handle=ConfigDB().get(uvm_root(), "", "COV_HANDLE")

    async def body(self):
        while self.cov_handle.get_my_coverage() < 100.00:
            sequence_packet=Pkt.create(f"packet")
            sequence_packet.randomize()
            await Timer(1, unit='step')
            await self.start_item(sequence_packet)
            await self.finish_item(sequence_packet)


        
        
