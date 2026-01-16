"""
MyCoverage: Functional coverage tracking for Half Adder verification.

Receives monitored transactions and samples coverage bins to ensure all input
combinations have been tested.
"""

from pyuvm import *
from HalfAdderCovergroup import HalfAdderCovergroup
import vsc

class MyCoverage(uvm_subscriber):
    """
    Coverage subscriber that tracks functional coverage for Half Adder.
    
    - Samples input combinations
    - Reports coverage percentage
    - Validates 100% coverage at end of test
    """

    def build_phase(self):
        """
        Build Phase: Instantiate covergroup.
        """
        self.cg=HalfAdderCovergroup()

    def write(self, pkt):
        """
        Called when monitor publishes a transaction.
        
        Samples the packet into covergroup to update coverage metrics.
        """
        self.cg.sample(pkt.a, pkt.b)

    def report_phase(self):
        """
        Report Phase: Check if coverage goal is met.
        - Logs PASS if 100% coverage achieved
        - Logs FAIL if coverage incomplete
        """
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
        """
        Return current coverage percentage.
        """
        return self.cg.get_coverage()
