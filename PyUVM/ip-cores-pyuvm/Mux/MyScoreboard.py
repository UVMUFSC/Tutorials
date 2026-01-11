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
                    f"PASS: X0={pkt.x0_i}, X1={pkt.x1_i}, X2={pkt.x2_i}, X3={pkt.x3_i}, SEL={pkt.sel_i} -> Y={pkt.y_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: X0={pkt.x0_i}, X1={pkt.x1_i}, X2={pkt.x2_i}, X3={pkt.x3_i}, SEL={pkt.sel_i}. ESPERADO Y={self.golden_model.y}. RECEBIDO Y={pkt.y_o}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard encontrou {self.num_errors} erros.")
        else:
            self.logger.info("TEST PASS: Todas as transações foram corretas.")
