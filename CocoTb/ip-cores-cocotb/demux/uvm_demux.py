# test_demux.py

import cocotb
from cocotb.triggers import Timer
from dataclasses import dataclass
import random

# 1. Transaction 
@dataclass
class DemuxTransaction:
    x_in: int
    sel: int

    y0_out: int = None
    y1_out: int = None
    y2_out: int = None
    y3_out: int = None

# 2. Driver 
class Driver:
    def __init__(self, dut):
        self.dut = dut

    async def drive(self, tr: DemuxTransaction):
        """Aplica a transação nas entradas do DEMUX."""
        self.dut.x_i.value = tr.x_in
        self.dut.sel_i.value = tr.sel
        
        await Timer(10, unit='ns')

# 3. Monitor 4
class Monitor:
    def __init__(self, dut):
        self.dut = dut
        self.scoreboard_callback = None 

    async def run(self):
        """Monitora a entrada e todas as saídas do DUT."""
        await Timer(9, unit='ns')
        
        # Lê todas as entradas e saídas para reconstruir a transação
        tr = DemuxTransaction(
            x_in=self.dut.x_i.value,
            sel=self.dut.sel_i.value.to_unsigned(),
            y0_out=self.dut.y0_o.value,
            y1_out=self.dut.y1_o.value,
            y2_out=self.dut.y2_o.value,
            y3_out=self.dut.y3_o.value
        )
        
        if self.scoreboard_callback:
            self.scoreboard_callback(tr)

# 4. Scoreboard 
class Scoreboard:
    def __init__(self, dut):
        self.dut = dut
        self.expected_queue = []
        self.errors = 0

    def ref_model(self, tr: DemuxTransaction):
        """O Golden Model para um DEMUX 1x4."""
        # Por padrão, todas as saídas devem ser 0
        y0_exp, y1_exp, y2_exp, y3_exp = 0, 0, 0, 0

        if tr.sel == 0:
            y0_exp = tr.x_in
        elif tr.sel == 1:
            y1_exp = tr.x_in
        elif tr.sel == 2:
            y2_exp = tr.x_in
        elif tr.sel == 3:
            y3_exp = tr.x_in
        
        self.expected_queue.append({
            "inputs": (tr.x_in, tr.sel),
            "outputs": (y0_exp, y1_exp, y2_exp, y3_exp)
        })

    def check_actual(self, actual_tr: DemuxTransaction):
        """Compara o resultado real com o esperado."""
        if not self.expected_queue:
            self.dut._log.error("[SCOREBOARD FAIL] Recebeu um resultado do DUT sem ter um esperado!")
            self.errors += 1
            return

        expected = self.expected_queue.pop(0)
        expected_outputs = expected["outputs"]
        actual_outputs = (actual_tr.y0_out, actual_tr.y1_out, actual_tr.y2_out, actual_tr.y3_out)
        
        inputs_str = f"x_in={actual_tr.x_in}, sel={actual_tr.sel}"
        if expected_outputs == actual_outputs:
            self.dut._log.info(f"[SCOREBOARD PASS] Entradas {inputs_str} -> y_out={actual_outputs}")
        else:
            self.dut._log.error(f"[SCOREBOARD FAIL] Para entradas {inputs_str}:")
            self.dut._log.error(f"  -> Esperado: y_out={expected_outputs}")
            self.dut._log.error(f"  -> Recebido: y_out={actual_outputs}")
            self.errors += 1

# 5. Environment 
class Environment:
    def __init__(self, dut):
        self.driver = Driver(dut)
        self.monitor = Monitor(dut)
        self.scoreboard = Scoreboard(dut)
        self.monitor.scoreboard_callback = self.scoreboard.check_actual

# 6. Test 
@cocotb.test()
async def demux_random_test(dut):
    """Testa o demux1x4 com verificação aleatória."""
    
    env = Environment(dut)
    
    num_random_tests = 50
    dut._log.info(f"Iniciando {num_random_tests} testes aleatórios...")

    for _ in range(num_random_tests):
        tr = DemuxTransaction(
            x_in=random.randint(0, 1),
            sel=random.randint(0, 3) 
        )
        
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    await Timer(20, unit='ns')
    assert env.scoreboard.errors == 0, f"Scoreboard encontrou {env.scoreboard.errors} erros."
    dut._log.info("Teste do demux1x4 concluído com sucesso!")