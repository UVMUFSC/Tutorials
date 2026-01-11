from pyuvm import *
from Pkt import Pkt

class MyMonitor(uvm_monitor):
    def __init__(self, name, parent):
        super().__init__(name, parent)
    
    def build_phase(self):
        self.ap=uvm_analysis_port("ap", self)
        self.bfm = ConfigDB().get(self, "", "BUS_BFM")

    async def run_phase(self):
        while True:
            result=await self.bfm.get_result()
            self.logger.debug(f"MONITORED {result}")
            packet=Pkt.create("monitored_packet")
            packet.a_i=result[0]
            packet.b_i=result[1]
            packet.carry_i=result[2]
            packet.carry_o=result[3]
            packet.sum_o=result[4]
            self.ap.write(packet)
    