
"""
MyScoreboard: Reference model verification for 4-bit Adder.

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

    num_errors = 0  # Counter for test failures

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
                    f"PASS: A_i={pkt.a_i}, B_i={pkt.b_i} -> S_o={pkt.sum_o}, C_o={pkt.carry_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: A_i={pkt.a_i}, B_i={pkt.b_i}. "
                    f"EXPECTED S_o={self.golden_model.s}, C_o={self.golden_model.c}. "
                    f"RECEIVED S_o={pkt.sum_o}, C_o={pkt.carry_o}"
                )

    def check_phase(self):
        """
        Check Phase: Final verdict on test results.
        
        Called after all phases complete. Reports overall pass/fail status
        and counts of errors found.
        """
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")

