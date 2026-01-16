"""
MyCoverage: Functional coverage collector for Mealy FSM.

Samples transactions from monitor and records coverage metrics. Provides
real-time coverage feedback to guide stimulus generation.
"""

from pyuvm import *
from MealyCovergroup import MealyCovergroup
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
        """
        Build Phase: Instantiate the coverage group.
        """
        self.cg=MealyCovergroup()

    def write(self, pkt):
        """
        Write method: sample state transition coverage.
        
        Encodes transition as: (prev_state << 2) | curr_state
        Example: 0->1 becomes (0<<2)|1 = 1
        
        Args:
            pkt: Packet with current_state and next_state
        """

        prev=int(pkt.current_state)
        curr=int(pkt.next_state)

        state=(prev << 2) | curr

        self.cg.sample(state)

    def report_phase(self):
        """
        Report phase: check if 100% coverage achieved.
        
        Verifies:
        - Coverage percentage
        - Asserts False if < 100%
        - Prints detailed report if incomplete
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
        """
        Get current coverage percentage.
        
        Returns:
            Float: Coverage percentage (0.0 to 100.0)
        """
        return self.cg.get_coverage()
    
    def get_report(self):
        """
        Print detailed coverage report.
        """
        print(get_coverage_report(details=True))
