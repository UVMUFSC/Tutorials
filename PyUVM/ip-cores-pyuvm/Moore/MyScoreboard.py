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
        self.logger.info("Scoreboard iniciando checagem...")
        while True:
            pkt = await self.fifo.get()

            if self.golden_model.check(pkt):
                self.logger.info(
                    f"PASS: PREVIOUS_STATE={pkt.previous_state}, NEXT={pkt.next_i}, RST={pkt.rst_i} -> OUT={pkt.out_o}, CURRENT_STATE={pkt.current_state}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: REVIOUS_STATE={pkt.previous_state}, NEXT={pkt.next_i}, RST={pkt.rst_i}. ESPERADO OUT={self.golden_model.out}, CURRENT_STATE={self.golden_model.current_state}. RECEBIDO OUT={pkt.out_o}, CURRENT_STATE={pkt.current_state}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard encontrou {self.num_errors} erros.")
        else:
            self.logger.info("TEST PASS: Todas as transações foram corretas.")
