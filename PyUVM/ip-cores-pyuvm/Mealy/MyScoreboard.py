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
                    f"PASS: CURRENT_STATE={pkt.current_state}, INPUT={pkt.mealy_i}, RST={pkt.rst_i} -> OUTPUT={pkt.mealy_o}, NEXT_STATE={pkt.next_state}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: CURRENT_STATE={pkt.current_state}, INPUT={pkt.mealy_i}, RST={pkt.rst_i}. EXPECTED OUTPUT={self.golden_model.mealy_o}, NEXT_STATE={self.golden_model.next_state}. RECEIVED OUTPUT={pkt.mealy_o}, NEXT_STATE={pkt.next_state}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
