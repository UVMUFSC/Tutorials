from pyuvm import *
from FullAdderCovergroup import HalfAdderCovergroup
import vsc

"""
MyCoverage: Functional coverage collector for Full Adder.

Samples transactions from monitor and records coverage metrics. Provides
real-time coverage feedback to guide stimulus generation.
"""

class MyCoverage(uvm_subscriber):
    """
    UVM coverage subscriber: collects functional coverage metrics.
    
    Operation:
    - Receives transactions via analysis export (connected to monitor)
    - Samples each transaction into covergroup
    - Tracks coverage percentage for stimulus termination condition
    """

    def build_phase(self):
        self.cg=HalfAdderCovergroup()

    def write(self, pkt):
        """
        Called when monitor publishes a transaction.
        
        Samples the packet into covergroup to update coverage metrics.
        """

        self.cg.sample(pkt.a_i, pkt.b_i, pkt.carry_i)

    def report_phase(self):

        cg_percent = self.cg.get_coverage()

        if cg_percent < 100.0:
            self.logger.error(
                f"Coverage FAIL: {100 - cg_percent:.2f}% uncovered."
            )
            assert False
        else:
            self.logger.info(f"Covered all operations (100.00%)")
            assert True

    def get_my_coverage(self):
        return self.cg.get_coverage()
