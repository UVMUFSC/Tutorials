"""
MyScoreboard: Reference model verification for Mux.

Compares DUT outputs against expected values from a golden model. Uses FIFO
to receive transactions from monitor and reports pass/fail for each.
"""

from pyuvm import *
from GoldenModel import GoldenModel

class MyScoreboard(uvm_scoreboard):
    """
    UVM scoreboard: verifies DUT correctness via golden model comparison.
    
    Operation:
    - Receives transactions from monitor via analysis FIFO
    - Runs golden model to compute expected result
    - Compares expected vs actual outputs
    - Logs PASS/FAIL and tracks error count
    """

    num_errors = 0

    def __init__(self, name, parent):
        super().__init__(name, parent)
    
    def build_phase(self):
        """
        Build Phase: Instantiate verification infrastructure.
        
        Creates FIFO for async transaction reception and golden model
        for reference output computation.
        """
        self.fifo = uvm_tlm_analysis_fifo("fifo", self)
        self.analysis_export = self.fifo.analysis_export
        self.golden_model = GoldenModel()

    async def run_phase(self):
        """
        Run Phase: Verify transactions as they arrive.
        
        Continuously:
        1. Wait for transaction from monitor FIFO
        2. Run golden model with same inputs
        3. Compare outputs: PASS if match, FAIL otherwise
        """
        self.logger.info("Scoreboard starting checks...")
        while True:
            pkt = await self.fifo.get()

            if self.golden_model.check(pkt):
                self.logger.info(
                    f"PASS: X0={pkt.x0_i}, X1={pkt.x1_i}, X2={pkt.x2_i}, X3={pkt.x3_i}, SEL={pkt.sel_i} -> Y={pkt.y_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: X0={pkt.x0_i}, X1={pkt.x1_i}, X2={pkt.x2_i}, X3={pkt.x3_i}, SEL={pkt.sel_i}. EXPECTED Y={self.golden_model.y}. RECEIVED Y={pkt.y_o}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
