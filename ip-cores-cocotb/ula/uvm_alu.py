# test_alu.py

import cocotb
from cocotb.triggers import Timer
from dataclasses import dataclass
import random
from enum import IntEnum

# 1. Enum para os Opcodes 
class Opcode(IntEnum):
    INC = 0b0000
    DEC = 0b0001
    ADD = 0b0010
    ADD_C = 0b0011
    SUB_B = 0b0100
    SUB = 0b0101
    SHIFT_R = 0b0110
    SHIFT_L = 0b0111
    AND_OP = 0b1000
    NAND = 0b1001
    OR = 0b1010
    NOR = 0b1011
    XOR = 0b1100
    XNOR = 0b1101
    NOT = 0b1110
    TRF_A = 0b1111

# 2. Transaction 
@dataclass
class AluTransaction:
    a: int
    b: int
    opcode: Opcode

    alu_out: int = None
    carry_out: int = None

# 3. Driver 
class Driver:
    def __init__(self, dut):
        self.dut = dut

    async def drive(self, tr: AluTransaction):
        """Aplica a transação nas entradas da ULA."""
        self.dut.A_i.value = tr.a
        self.dut.B_i.value = tr.b
        self.dut.opcode_i.value = tr.opcode.value
        await Timer(10, unit='ns')

# 4. Monitor 
class Monitor:
    def __init__(self, dut):
        self.dut = dut
        self.scoreboard_callback = None 

    async def run(self):
        """Monitora todas as entradas e saídas da ULA."""
        await Timer(9, unit='ns')
        
        tr = AluTransaction(
            a=self.dut.A_i.value.to_unsigned(),
            b=self.dut.B_i.value.to_unsigned(),
            opcode=Opcode(self.dut.opcode_i.value.to_unsigned()),
            alu_out=self.dut.alu_o.value.to_unsigned(),
            carry_out=self.dut.carry_o.value
        )
        
        if self.scoreboard_callback:
            self.scoreboard_callback(tr)

# 5. Scoreboard 
class Scoreboard:
    def __init__(self, dut):
        self.dut = dut
        self.expected_queue = []
        self.errors = 0
        self.N = len(dut.A_i) 
        self.MASK = (1 << self.N) - 1 

    def ref_model(self, tr: AluTransaction):
        """O Golden Model que replica a lógica da ULA em Python."""
        
        carry_expected = 1 if (tr.a + tr.b) > self.MASK else 0

        
        result = 0
        if tr.opcode == Opcode.INC:
            result = tr.a + 1
        elif tr.opcode == Opcode.DEC:
            result = tr.a - 1
        elif tr.opcode == Opcode.ADD:
            result = tr.a + tr.b
        elif tr.opcode == Opcode.ADD_C:
            result = tr.a + tr.b + 1
        elif tr.opcode == Opcode.SUB_B:
            result = tr.a - tr.b
        elif tr.opcode == Opcode.SUB:
            result = tr.a - tr.b - 1
        elif tr.opcode == Opcode.SHIFT_R:
            result = tr.a >> tr.b
        elif tr.opcode == Opcode.SHIFT_L:
            result = tr.a << tr.b
        elif tr.opcode == Opcode.AND_OP:
            result = tr.a & tr.b
        elif tr.opcode == Opcode.NAND:
            result = ~(tr.a & tr.b)
        elif tr.opcode == Opcode.OR:
            result = tr.a | tr.b
        elif tr.opcode == Opcode.NOR:
            result = ~(tr.a | tr.b)
        elif tr.opcode == Opcode.XOR:
            result = tr.a ^ tr.b
        elif tr.opcode == Opcode.XNOR:
            result = ~(tr.a ^ tr.b)
        elif tr.opcode == Opcode.TRF_A:
            result = tr.a
        else:
            result = 0
        
        alu_expected = result & self.MASK

        self.expected_queue.append({
            "inputs": (tr.a, tr.b, tr.opcode.name),
            "outputs": (alu_expected, carry_expected)
        })

    def check_actual(self, actual_tr: AluTransaction):
        if not self.expected_queue:
            self.dut._log.error("[SCOREBOARD FAIL] Recebeu um resultado sem ter um esperado!")
            self.errors += 1
            return

        expected = self.expected_queue.pop(0)
        expected_alu, expected_c = expected["outputs"]
        actual_alu, actual_c = actual_tr.alu_out, actual_tr.carry_out
        
        inputs_str = f"A={actual_tr.a}, B={actual_tr.b}, opcode={actual_tr.opcode.name}"
        if expected_alu == actual_alu and expected_c == actual_c:
            self.dut._log.info(f"[SCOREBOARD PASS] {inputs_str} -> alu={actual_alu}, carry={actual_c}")
        else:
            self.dut._log.error(f"[SCOREBOARD FAIL] Para {inputs_str}:")
            self.dut._log.error(f"  -> Esperado: alu={expected_alu}, carry={expected_c}")
            self.dut._log.error(f"  -> Recebido: alu={actual_alu}, carry={actual_c}")
            self.errors += 1

# 6. Environment 
class Environment:
    def __init__(self, dut):
        self.driver = Driver(dut)
        self.monitor = Monitor(dut)
        self.scoreboard = Scoreboard(dut)
        self.monitor.scoreboard_callback = self.scoreboard.check_actual

# 7. Test 
@cocotb.test()
async def alu_random_test(dut):
    """Testa a ULA com casos direcionados e verificação aleatória."""
    
    env = Environment(dut)
    N = len(dut.A_i)
    MAX_VAL = (1 << N) - 1

    # Parte 1: Teste direcionado para cada opcode
    dut._log.info("Iniciando teste direcionado para cada opcode...")
    # Usamos valores fixos para A e B para testar cada operação
    a_fixed, b_fixed = 170, 85 # 10101010 e 01010101 em binário
    for opcode in Opcode:
        tr = AluTransaction(a=a_fixed, b=b_fixed, opcode=opcode)
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    # Parte 2: Teste aleatório;
    num_random_tests = 50 # ideal mais testes para ALU.
    dut._log.info(f"Iniciando {num_random_tests} testes aleatórios...")
    opcodes = list(Opcode) 
    for _ in range(num_random_tests):
        tr = AluTransaction(
            a=random.randint(0, MAX_VAL),
            b=random.randint(0, MAX_VAL),
            opcode=random.choice(opcodes)
        )
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    await Timer(20, unit='ns')
    assert env.scoreboard.errors == 0, f"Scoreboard encontrou {env.scoreboard.errors} erros."
    dut._log.info("Teste da ULA concluído com sucesso!")