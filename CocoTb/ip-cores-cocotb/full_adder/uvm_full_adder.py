import cocotb
from cocotb.triggers import Timer
from dataclasses import dataclass
import random

# 1. Transaction
@dataclass
class FullAdderTransaction:
    a: int
    b: int
    carry_in: int

    sum_out: int = None
    carry_out: int = None

# 2. Driver 
class Driver:
    def __init__(self, dut):
        self.dut = dut

    async def drive(self, tr: FullAdderTransaction):
        """Aplica a transação no DUT e espera um "ciclo"."""
        self.dut.a_i.value = tr.a
        self.dut.b_i.value = tr.b
        self.dut.carry_i.value = tr.carry_in
        
        await Timer(10, unit='ns') 

# 3. Monitor 
class Monitor:
    def __init__(self, dut):
        self.dut = dut
        self.scoreboard_callback = None 

    async def run(self):
        """Monitora as saídas do DUT e reconstrói a transação."""
        await Timer(9, unit='ns') 
        
        sum_val = self.dut.sum_o.value
        carry_val = self.dut.carry_o.value

        a_val = self.dut.a_i.value
        b_val = self.dut.b_i.value
        carry_in_val = self.dut.carry_i.value

        tr = FullAdderTransaction(
            a=a_val, b=b_val, carry_in=carry_in_val,
            sum_out=sum_val, carry_out=carry_val
        )
        
        if self.scoreboard_callback:
            self.scoreboard_callback(tr)

# 4. Scoreboard 
class Scoreboard:
    def __init__(self):
        self.expected_queue = []
        self.errors = 0

    def ref_model(self, tr: FullAdderTransaction):
        """O Golden Model para o full adder."""
        temp_sum = tr.a + tr.b + tr.carry_in
        sum_expected = temp_sum % 2  
        carry_expected = 1 if temp_sum >= 2 else 0 

        self.expected_queue.append({
            "inputs": (tr.a, tr.b, tr.carry_in),
            "outputs": (sum_expected, carry_expected)
        })

    def check_actual(self, actual_tr: FullAdderTransaction):
        """Compara o resultado real (do Monitor) com o esperado (do ref_model)."""
        if not self.expected_queue:
            print("[SCOREBOARD FAIL] Recebeu um resultado do DUT sem ter um esperado!")
            self.errors += 1
            return

        expected = self.expected_queue.pop(0)
        expected_s, expected_c = expected["outputs"]
        
        actual_s, actual_c = actual_tr.sum_out, actual_tr.carry_out

        inputs = (actual_tr.a, actual_tr.b, actual_tr.carry_in)
        if expected_s == actual_s and expected_c == actual_c:
            print(f"[SCOREBOARD PASS] Entradas {inputs} -> sum={actual_s}, carry={actual_c}")
        else:
            print(f"[SCOREBOARD FAIL] Para entradas {inputs}:")
            print(f"  -> Esperado: sum={expected_s}, carry={expected_c}")
            print(f"  -> Recebido: sum={actual_s}, carry={actual_c}")
            self.errors += 1

# 5. Environment 
class Environment:
    def __init__(self, dut):
        self.dut = dut
        self.driver = Driver(dut)
        self.monitor = Monitor(dut)
        self.scoreboard = Scoreboard()
        self.monitor.scoreboard_callback = self.scoreboard.check_actual

# 6. Test
@cocotb.test()
async def full_adder_random_test(dut):
    """
    Testa o full_adder usando uma combinação de casos de canto direcionados
    e verificação aleatória massiva.
    """
    
    env = Environment(dut)
    
    # --- Parte 1: Teste Direcionado de Casos de Canto ---
    # Estes são os casos que QUEREMOS garantir que sejam testados.
    corner_cases = [
        (0, 0, 0),  # Caso mais simples
        (0, 0, 1),
        (1, 1, 0),
        (1, 1, 1),  # Caso de overflow máximo
    ]

    dut._log.info("Iniciando teste de casos de canto...")
    for a, b, carry_in in corner_cases:
        tr = FullAdderTransaction(a=a, b=b, carry_in=carry_in)
        
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    # --- Parte 2: Teste Aleatório Massivo ---
    num_random_tests = 50  # Aumente este número para uma verificação mais completa

    dut._log.info(f"Iniciando {num_random_tests} testes aleatórios...")
    for i in range(num_random_tests):
        # Gera uma transação com valores aleatórios
        tr = FullAdderTransaction(
            a=random.randint(0, 1),
            b=random.randint(0, 1),
            carry_in=random.randint(0, 1)
        )
        
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    await Timer(20, unit='ns') 

    assert env.scoreboard.errors == 0, f"Scoreboard encontrou {env.scoreboard.errors} erros."
    assert not env.scoreboard.expected_queue, "Algumas transações esperadas não foram verificadas."
    dut._log.info("Teste aleatório concluído com sucesso!")