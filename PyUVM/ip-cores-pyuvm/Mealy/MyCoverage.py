from pyuvm import *
from MealyCovergroup import MealyCovergroup
import vsc
from vsc import get_coverage_report

class MyCoverage(uvm_subscriber):
    def build_phase(self):
        self.cg=MealyCovergroup()

    def write(self, pkt):

        prev=int(pkt.current_state)
        curr=int(pkt.next_state)

        state=(prev << 2) | curr

        self.cg.sample(state)

    def report_phase(self):

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
        return self.cg.get_coverage()
    
    def get_report(self):
        print(get_coverage_report(details=True))
