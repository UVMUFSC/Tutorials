import cocotb
from cocotb.triggers import Timer
from dataclasses import dataclass

# 1. Transaction
@dataclass
class HalfAdderTransaction:
    a: int
    b: int
    s: int = None
    c: int = None

# 2. Driver
class Driver:
    def __init__(self, dut):
        self.dut = dut

    async def drive(self, tr: HalfAdderTransaction):
        self.dut.a.value = tr.a
        self.dut.b.value = tr.b
        await Timer(10, unit='ns') 

# 3. Monitor
class Monitor:
    def __init__(self, dut):
        self.dut = dut
        self.scoreboard_callback = None 

    async def run(self):
        await Timer(9, unit='ns') 
        
        s_val = self.dut.s.value
        c_val = self.dut.c.value
        a_val = self.dut.a.value
        b_val = self.dut.b.value

        tr = HalfAdderTransaction(a=a_val, b=b_val, s=s_val, c=c_val)
        
        if self.scoreboard_callback:
            self.scoreboard_callback(tr)

# 4. Scoreboard
class Scoreboard:
    def __init__(self):
        self.expected_queue = []
        self.errors = 0

    def ref_model(self, tr: HalfAdderTransaction):
        s_expected = tr.a ^ tr.b
        c_expected = tr.a & tr.b
        self.expected_queue.append({
            "inputs": (tr.a, tr.b),
            "outputs": (s_expected, c_expected)
        })

    def check_actual(self, actual_tr: HalfAdderTransaction):
        if not self.expected_queue:
            print("[SCOREBOARD FAIL] Recebeu um resultado do DUT sem ter um esperado!")
            self.errors += 1
            return

        expected = self.expected_queue.pop(0)
        expected_s, expected_c = expected["outputs"]
        actual_s, actual_c = actual_tr.s, actual_tr.c

        if expected_s == actual_s and expected_c == actual_c:
            print(f"[SCOREBOARD PASS] a={actual_tr.a}, b={actual_tr.b} -> s={actual_s}, c={actual_c}")
        else:
            print(f"[SCOREBOARD FAIL] Para a={actual_tr.a}, b={actual_tr.b}:")
            print(f"  -> Esperado: s={expected_s}, c={expected_c}")
            print(f"  -> Recebido: s={actual_s}, c={actual_c}")
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
async def half_adder_uvm_test(dut):
    """Verificação de half-adder utilizando UVM."""
    
    env = Environment(dut)

    test_vectors = [(0,0), (0,1), (1,0), (1,1)]

    for a, b in test_vectors:
        tr = HalfAdderTransaction(a=a, b=b)
        env.scoreboard.ref_model(tr)
        await env.driver.drive(tr)
        await env.monitor.run()

    assert env.scoreboard.errors == 0, f"Scoreboard encontrou {env.scoreboard.errors} erros."
    assert not env.scoreboard.expected_queue, "Algumas transações esperadas não foram verificadas."