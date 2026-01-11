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
                    f"PASS: X={pkt.x_i}, SEL={pkt.sel_i} -> Y0={pkt.y0_o}, Y1={pkt.y1_o}, Y2={pkt.y2_o}, Y3={pkt.y3_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: X={pkt.x_i}, SEL={pkt.sel_i}. ESPERADO Y0={self.golden_model.y0}, Y1={self.golden_model.y1}, Y2={self.golden_model.y2}, Y3={self.golden_model.y3}. RECEBIDO Y0={pkt.y0_o}, Y1={pkt.y1_o}, Y2={pkt.y2_o}, Y3={pkt.y3_o}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard encontrou {self.num_errors} erros.")
        else:
            self.logger.info("TEST PASS: Todas as transações foram corretas.")
