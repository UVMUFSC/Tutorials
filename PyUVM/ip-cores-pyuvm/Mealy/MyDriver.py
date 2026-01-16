"""
MyDriver: UVM driver for Mealy FSM.

Receives transactions from the sequencer and drives them to the DUT via BFM.
Actuates DUT inputs and coordinates with BFM for proper timing and handshake.
"""

from pyuvm import *

class MyDriver(uvm_driver):
    """
    UVM driver: applies transactions to the DUT.
    
    Operation:
    - Waits for transactions from sequencer
    - Sends each transaction to BFM for DUT input application
    - Signals completion before requesting next transaction
    """

    def __init__(self, name, parent):
        super().__init__(name, parent)

    def build_phase(self):
        """
        Build Phase: Retrieve DUT interface (BFM) from ConfigDB.
        
        The BFM handles low-level DUT signal manipulation and timing.
        """
        self.bfm = ConfigDB().get(self, "", "BUS_BFM")

    async def run_phase(self):
        """
        Run Phase: Drive transactions to DUT as they arrive.
        
        Loop:
        1. Wait for transaction from sequencer
        2. Send to BFM for DUT input application
        3. Signal completion and request next
        """
        while True:
            packet=await self.seq_item_port.get_next_item()
            await self.bfm.send_pkt(packet)
            self.seq_item_port.item_done()
