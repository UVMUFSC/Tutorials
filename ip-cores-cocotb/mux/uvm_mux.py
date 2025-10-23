import cocotb
from cocotb.triggers import Timer
from dataclasses import dataclass
import random

# 1. Transaction 
@dataclass
class MuxTransaction:
    x0: int
    x1: int
    x2: int
    x3: int
    
    sel: int

    y_out: int = None

# 2. Driver 
class Driver:
    def __init__(self, dut):
        self.dut = dut

    async def drive(self, tr: MuxTransaction):
        """Aplica a transação nas entradas do MUX."""
        self.dut.x0_i.value = tr.x0
        self.dut.x1_i.value = tr.x1
        self.dut.x2_i.value = tr.x2
        self.dut.x3_i.value = tr.x3
        self.dut.sel_i.value = tr.sel 
        
        await Timer(10, unit='ns')

# 3. Monitor 
class Monitor:
    def __init__(self, dut):
        self.dut = dut
        self.scoreboard_callback = None 

    async def run(self):
        """Monitora todas as entradas e a saída do DUT."""
        await Timer(9, unit='ns')
        
        tr = MuxTransaction(
            x0=self.dut.x0_i.value,
            x1=self.dut.x1_i.value,
            x2=self.dut.x2_i.value,
            x3=self.dut.x3_i.value,
            sel=self.dut.sel_i.value.to_unsigned(),
            y_out=self.dut.y_o.value
        )
        
        if self.scoreboard_callback:
            self.scoreboard_callback(tr)

# 4. Scoreboard 
class Scoreboard:
    def __init__(self, dut):
        self.dut = dut
        self.expected_queue = []
        self.errors = 0

    def ref_model(self, tr: MuxTransaction):
        """O Golden Model para um MUX 4x1."""
        y_expected = 0
        if tr.sel == 0:
            y_expected = tr.x0
        elif tr.sel == 1:
            y_expected = tr.x1
        elif tr.sel == 2:
            y_expected = tr.x2
        elif tr.sel == 3:
            y_expected = tr.x3
        
        self.expected_queue.append({
            "inputs": (tr.x0, tr.x1, tr.x2, tr.x3, tr.sel),
            "output": y_expected
        })

    def check_actual(self, actual_tr: MuxTransaction):
        """Compara o resultado real com o esperado."""
        if not self.expected_queue:
            self.dut._log.error("[SCOREBOARD FAIL] Recebeu um resultado do DUT sem ter um esperado!")
            self.errors += 1
            return

        expected = self.expected_queue.pop(0)
        expected_y = expected["output"]
        actual_y = actual_tr.y_out
        
        inputs_str = f"x=({actual_tr.x0},{actual_tr.x1},{actual_tr.x2},{actual_tr.x3}), sel={actual_tr.sel}"
        if expected_y == actual_y:
            self.dut._log.info(f"[SCOREBOARD PASS] Entradas {inputs_str} -> y={actual_y}")
        else:
            self.dut._log.error(f"[SCOREBOARD FAIL] Para entradas {inputs_str}:")
            self.dut._log.error(f"  -> Esperado: y={expected_y}")
            self.dut._log.error(f"  -> Recebido: y={actual_y}")
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
async def mux_random_test(dut):
    """Testa o mux4x1 com verificação aleatória."""
    
    env = Environment(dut)
    
    num_random_tests = 50
    dut._log.info(f"Iniciando {num_random_tests} testes aleatórios...")

    for _ in range(num_random_tests):
        tr = MuxTransaction(
            x0=random.randint(0, 1),
            x1=random.randint(0, 1),
            x2=random.randint(0, 1),
            x3=random.randint(0, 1),
            sel=random.randint(0, 3) 
        )
        
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    await Timer(20, unit='ns')
    assert env.scoreboard.errors == 0, f"Scoreboard encontrou {env.scoreboard.errors} erros."
    dut._log.info("Teste do mux4x1 concluído com sucesso!")