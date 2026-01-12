from pyuvm import *
from GoldenModel import GoldenModel

class MyScoreboard(uvm_scoreboard):

    num_errors=0

    def __init__(self, name, parent):
        super().__init__(name,parent)
    
    def build_phase(self):
        self.fifo=uvm_tlm_analysis_fifo("fifo", self)
        self.analysis_export=self.fifo.analysis_export
        self.golden_model=GoldenModel()

    async def run_phase(self):
        self.logger.info("Scoreboard starting checks...")
        while True:
            pkt = await self.fifo.get()

            if self.golden_model.check(pkt):
                self.logger.info(
                    f"PASS: A_i={pkt.a_i}, B_i={pkt.b_i}, C_i={pkt.carry_i} -> S_o={pkt.sum_o}, C_o={pkt.carry_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: A_i={pkt.a_i}, B_i={pkt.b_i}, C_i={pkt.carry_i}. EXPECTED S_o={self.golden_model.s}, C_o={self.golden_model.c}. RECEIVED S_o={pkt.sum_o}, C_o={pkt.carry_o}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")

