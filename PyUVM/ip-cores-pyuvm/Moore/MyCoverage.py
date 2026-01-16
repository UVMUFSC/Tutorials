"""
MyCoverage: Functional coverage collector for Moore FSM.

Samples transactions from monitor and records coverage metrics. Provides
real-time coverage feedback to guide stimulus generation.
"""

from pyuvm import *
from MooreCovergroup import MooreCovergroup
import vsc
from vsc import get_coverage_report

class MyCoverage(uvm_subscriber):
    """
    UVM coverage subscriber: collects functional coverage metrics.
    
    Operation:
    - Receives transactions via analysis export (connected to monitor)
    - Samples each transaction into covergroup
    - Tracks coverage percentage for stimulus termination condition
    """
    def build_phase(self):
        self.cg=MooreCovergroup()

    def write(self, pkt):

        prev=int(pkt.previous_state)
        curr=int(pkt.current_state)

        state=(prev << 3) | curr

        self.cg.sample(pkt.next_i, state)

    def report_phase(self):
        """Report phase - check and report coverage results.
        
        Checks:
            - Coverage percentage against 100% target
            - Reports uncovered scenarios if incomplete
            - Asserts PASS/FAIL based on coverage
        """

        cg_percent = self.cg.get_coverage()

        if cg_percent < 100.0:
            self.logger.error(
                f"Coverage FAIL: {100 - cg_percent:.2f}% uncovered."
            )
            self.get_report()
            assert False
        else:
            self.logger.info(f"Covered all operations (100.00%)")
            assert True

    def get_my_coverage(self):
        """Get current coverage percentage.
        
        Returns:
            Coverage percentage (0.0 to 100.0)
        """
        return self.cg.get_coverage()
    
    def get_report(self):
        """Print detailed coverage report.
        
        Shows which bins are covered and which are missing.
        """
        print(get_coverage_report(details=True))
