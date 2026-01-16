from pyuvm import *
from Pkt import Pkt
from MyCoverage import MyCoverage
from cocotb.triggers import Timer

"""
MySequence: Coverage-driven stimulus generator for Mux.

Generates random test vectors in a loop until functional coverage reaches 100%.
Implements the main stimulus strategy for verifying all operational scenarios.
"""

class MySequence(uvm_sequence):
    """
    Coverage-driven sequence: generates transactions until coverage goal is met.
    
    Operation:
    - Retrieves coverage handle from ConfigDB to monitor progress
    - Loop: randomize packet, send to sequencer until coverage = 100%
    - Ensures all functional scenarios are exercised
    """

    def __init__(self, name):
        super().__init__(name)
        # Retrieve coverage handle from ConfigDB
        self.cov_handle=ConfigDB().get(uvm_root(), "", "COV_HANDLE")

    async def body(self):
        """
        Main stimulus generation loop.
        
        Generates random test vectors until coverage goal is met:
        1. Check coverage percentage
        2. Create and randomize new packet
        3. Send packet to sequencer for driver application
        4. Repeat until 100% coverage achieved
        """
        while self.cov_handle.cg.get_coverage() < 100.00:
            sequence_packet=Pkt.create(f"packet")
            sequence_packet.randomize()
            await Timer(1, unit='step')
            await self.start_item(sequence_packet)
            await self.finish_item(sequence_packet)


        
        
