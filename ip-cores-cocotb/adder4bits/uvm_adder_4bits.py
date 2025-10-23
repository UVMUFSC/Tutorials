# test_adder_4bits.py - VERSÃO CORRIGIDA

import cocotb
from cocotb.triggers import Timer
from dataclasses import dataclass
import random

# 1. Transaction
@dataclass
class Adder4BitTransaction:
    a: int
    b: int
    sum_out: int = None
    carry_out: int = None

# 2. Driver
class Driver:
    def __init__(self, dut):
        self.dut = dut

    async def drive(self, tr: Adder4BitTransaction):
        self.dut.a_i.value = tr.a
        self.dut.b_i.value = tr.b
        await Timer(10, unit='ns')

# 3. Monitor 
class Monitor:
    def __init__(self, dut):
        self.dut = dut
        self.scoreboard_callback = None 

    async def run(self):
        await Timer(9, unit='ns')
        
        # Para vetores [3:0], usamos .to_unsigned()
        sum_val = self.dut.s_o.value.to_unsigned()
        a_val = self.dut.a_i.value.to_unsigned()
        b_val = self.dut.b_i.value.to_unsigned()
        
        # Para um sinal de 1 bit, usamos apenas .value
        carry_val = self.dut.c_o.value

        tr = Adder4BitTransaction(
            a=a_val, b=b_val,
            sum_out=sum_val, carry_out=carry_val
        )
        
        if self.scoreboard_callback:
            self.scoreboard_callback(tr)

# 4. Scoreboard
class Scoreboard:
    def __init__(self, dut):
        self.dut = dut
        self.expected_queue = []
        self.errors = 0

    def ref_model(self, tr: Adder4BitTransaction):
        temp_sum = tr.a + tr.b
        sum_expected = temp_sum & 0xF
        carry_expected = 1 if temp_sum > 15 else 0
        self.expected_queue.append({
            "inputs": (tr.a, tr.b),
            "outputs": (sum_expected, carry_expected)
        })

    def check_actual(self, actual_tr: Adder4BitTransaction):
        if not self.expected_queue:
            self.dut._log.error("[SCOREBOARD FAIL] Recebeu um resultado do DUT sem ter um esperado!")
            self.errors += 1
            return

        expected = self.expected_queue.pop(0)
        expected_s, expected_c = expected["outputs"]
        actual_s, actual_c = actual_tr.sum_out, actual_tr.carry_out

        inputs = (actual_tr.a, actual_tr.b)
        if expected_s == actual_s and expected_c == actual_c:
            self.dut._log.info(f"[SCOREBOARD PASS] Entradas {inputs} -> sum={actual_s}, carry={actual_c}")
        else:
            self.dut._log.error(f"[SCOREBOARD FAIL] Para entradas {inputs}:")
            self.dut._log.error(f"  -> Esperado: sum={expected_s}, carry={expected_c}")
            self.dut._log.error(f"  -> Recebido: sum={actual_s}, carry={actual_c}")
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
async def adder_4bits_random_test(dut):
    env = Environment(dut)
    dut._log.info("Iniciando teste de casos de canto...")
    corner_cases = [
        (0, 0),      # Somando zero
        (15, 0),     # Somando com o valor máximo
        (8, 7),      # Resultado máximo sem carry out (15)
        (8, 8),      # Resultado mínimo com carry out (16)
        (15, 15),    # Soma máxima possível
    ]
    for a, b in corner_cases:
        tr = Adder4BitTransaction(a=a, b=b)
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    num_random_tests = 50
    dut._log.info(f"Iniciando {num_random_tests} testes aleatórios...")
    for _ in range(num_random_tests):
        a_rand = random.randint(0, 15)
        b_rand = random.randint(0, 15)
        tr = Adder4BitTransaction(a=a_rand, b=b_rand)
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    await Timer(20, unit='ns')
    assert env.scoreboard.errors == 0, f"Scoreboard encontrou {env.scoreboard.errors} erros."
    dut._log.info("Teste do adder_4bits concluído com sucesso!")