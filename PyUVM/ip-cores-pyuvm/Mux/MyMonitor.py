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
            packet=Pkt("monitored_packet")
            packet.x0_i=result[0]
            packet.x1_i=result[1]
            packet.x2_i=result[2]
            packet.x3_i=result[3]
            packet.sel_i=result[4]
            packet.y_o=result[5]
            self.ap.write(packet)
    