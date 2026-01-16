"""Moore FSM UVM Monitor.

Observes DUT outputs and state transitions via the BFM.
Converts BFM results into UVM transaction packets for analysis.

Monitor Flow:
- Retrieve results from BFM monitor queue
- Create transaction packet
- Populate with inputs, outputs, and state information
- Broadcast via analysis port
"""

from pyuvm import *
from Pkt import Pkt

class MyMonitor(uvm_monitor):
    """Monitor for Moore FSM verification.
    
    Responsibilities:
        - Observe DUT responses from BFM
        - Create and populate transaction packets
        - Broadcast transactions to scoreboard and coverage
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
            packet.next_i=result[0]
            packet.rst_i=result[1]
            packet.out_o=result[2]
            packet.previous_state=result[3]
            packet.current_state=result[4]
            self.ap.write(packet)
    