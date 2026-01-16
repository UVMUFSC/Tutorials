"""
MyScoreboard: Reference model verification for Moore FSM.

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

    num_errors=0

    def __init__(self, name, parent):
        """Initialize scoreboard.
        
        Args:
            name: Scoreboard identifier
            parent: Parent component in UVM hierarchy
        """
        super().__init__(name,parent)
    
    def build_phase(self):
        """
        Build Phase: Instantiate verification infrastructure.
        
        Creates FIFO for async transaction reception and golden model
        for reference output computation.
        """
        self.fifo=uvm_tlm_analysis_fifo("fifo", self)
        self.analysis_export=self.fifo.analysis_export
        self.golden_model=GoldenModel()

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
                    f"PASS: PREVIOUS_STATE={pkt.previous_state}, NEXT={pkt.next_i}, RST={pkt.rst_i} -> OUT={pkt.out_o}, CURRENT_STATE={pkt.current_state}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: PREVIOUS_STATE={pkt.previous_state}, NEXT={pkt.next_i}, RST={pkt.rst_i}. EXPECTED OUT={self.golden_model.out}, CURRENT_STATE={self.golden_model.current_state}. RECEIVED OUT={pkt.out_o}, CURRENT_STATE={pkt.current_state}"
                )

    def check_phase(self):
        """Check phase - report final verification status.
        
        Reports:
            - PASS if num_errors == 0
            - FAIL if any errors detected
        """
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
