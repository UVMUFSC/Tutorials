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
            packet.a=result[0]
            packet.b=result[1]
            packet.s=result[2]
            packet.c=result[3]
            self.ap.write(packet)
    