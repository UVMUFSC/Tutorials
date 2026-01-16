from pyuvm import *
from Adder4BitsCovergroup import Adder4BitsCovergroup
import vsc



"""
MyCoverage: Functional coverage collector for 4-bit Adder.

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
        """
        Build Phase: Instantiate the coverage group.
        """
        self.cg = Adder4BitsCovergroup()

    def write(self, pkt):
        """
        Called when monitor publishes a transaction.
        
        Samples the packet into covergroup to update coverage metrics.
        """
        self.cg.sample(pkt.a_i, pkt.b_i)

    def report_phase(self):
        """
        Report Phase: Report coverage results at end of simulation.
        """
        cg_percent = self.cg.get_coverage()
        if cg_percent < 100.0:
            self.logger.error(
                f"Coverage FAIL: {100 - cg_percent:.2f}% uncovered."
            )
            assert False
        else:
            self.logger.info(f"Covered all operations (100.00%)")
            self.cg.report()
            assert True

    def get_my_coverage(self):
        """
        Return current coverage percentage.
        """
        return self.cg.get_coverage()
