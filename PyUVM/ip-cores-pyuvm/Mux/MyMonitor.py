"""
MyMonitor: UVM monitor for 4x1 Mux.

Observes DUT outputs via BFM and publishes transactions to analysis port.
Converts raw BFM results into packet objects for consumption by scoreboard
and coverage components.
"""

from pyuvm import *
from Pkt import Pkt

class MyMonitor(uvm_monitor):
    """
    UVM monitor: observes DUT outputs and publishes transactions.

    Operation:
    - Waits for results from BFM (Bus Functional Model)
    - Converts raw results into Pkt objects
    - Writes packets to analysis port for verification/coverage
    """

    def __init__(self, name, parent):
        super().__init__(name, parent)
    
    def build_phase(self):
        """
        Build Phase: Set up analysis port and retrieve BFM handle.
        
        Analysis port enables broadcasting observed transactions to
        multiple subscribers (scoreboard, coverage).
        """
        self.ap=uvm_analysis_port("ap", self)
        self.bfm = ConfigDB().get(self, "", "BUS_BFM")

    async def run_phase(self):
        """
        Run Phase: Observe DUT outputs and publish as packets.

        Continuously:
        1. Wait for result from BFM
        2. Convert result tuple into Pkt object
        3. Write packet to analysis port
        """
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
    