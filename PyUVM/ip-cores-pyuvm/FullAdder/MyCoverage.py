from pyuvm import *
from FullAdderCovergroup import HalfAdderCovergroup
import vsc

class MyCoverage(uvm_subscriber):
    def build_phase(self):
        self.cg=HalfAdderCovergroup()

    def write(self, pkt):

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
