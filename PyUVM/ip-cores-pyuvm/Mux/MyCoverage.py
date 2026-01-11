from pyuvm import *
from MuxCovergroup import MuxCovergroup
import vsc

class MyCoverage(uvm_subscriber):
    def build_phase(self):
        self.cg=MuxCovergroup()

    def write(self, pkt):

        self.cg.sample(pkt.x0_i, pkt.x1_i, pkt.x2_i, pkt.x3_i, pkt.sel_i)

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
