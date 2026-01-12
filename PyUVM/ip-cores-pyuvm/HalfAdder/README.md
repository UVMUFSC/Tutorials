# Tutorial: Verifying a Half-Adder using PyUVM

This tutorial verifies `half_adder.sv` using PyUVM. Because the input space is small (2 bits), the README includes both directed exhaustive checks and the standard PyUVM pattern with a Scoreboard + GoldenModel.

## Goals
- Demonstrate the PyUVM pattern on a small DUT and use directed tests for exhaustive checking.
- Show how the Scoreboard and GoldenModel interact for simple combinational logic.

## File Structure
```bash
ip-cores-pyuvm/HalfAdder/
├── half_adder.sv
├── Makefile
├── MyTest.py
├── MyEnv.py
├── MyAgent.py
├── MyDriver.py
├── MyMonitor.py
├── MyScoreboard.py
├── GoldenModel.py
├── MyCoverage.py
├── MySequence.py
├── Pkt.py
└── HalfAdderWrapper.py
```

## The DUT
The Half-Adder computes sum = a ^ b and carry = a & b.

## Verification Logic
- `MyTest`: instantiates the wrapper (BFM), stores it in `ConfigDB`, and starts the environment and sequences.
- `MyEnv`: creates `MyAgent`, `MyScoreboard`, and `MyCoverage` and wires analysis ports (connect the monitor analysis export to `scoreboard.analysis_export`).
- `MyAgent`: contains `MySequencer`, `MyDriver`, and `MyMonitor`.
  - `MyDriver` obtains the BFM from `ConfigDB` and applies stimulus to the DUT.
  - `MyMonitor` samples DUT/wrapper signals, converts them to `Pkt` transactions and writes them to the analysis ports.
- `MyScoreboard`: receives transactions (via `uvm_tlm_analysis_fifo`), compares DUT outputs with `GoldenModel` expectations in `run_phase()`, logs PASS/FAIL per transaction, and reports final result in `check_phase()`.
- `MyCoverage`: samples `pyvsc` covergroups and asserts coverage goals in `report_phase()` when targets are met.

Note: Sequences typically call `env.scoreboard.ref_model(tr)` (or rely on an internal golden model in the scoreboard) to register expectations before the driver applies signals.

## Running the Verification
```bash
cd ip-cores-pyuvm/HalfAdder
# (optional) activate your virtualenv
source venv_cocotb/bin/activate
make
```

## Scoreboard & GoldenModel (actual implementations)
The real `GoldenModel.py` and `MyScoreboard.py` for this module are intentionally small and match the examples used in the project.

### GoldenModel (actual implementation)
```python
class GoldenModel():
    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):
        self.s=packet.a ^ packet.b
        self.c = packet.a & packet.b

        if packet.s == self.s and packet.c == self.c:
            return True
        else:
            return False
```

### Scoreboard (actual implementation)
```python
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
                    f"PASS: A={pkt.a}, B={pkt.b} -> S={pkt.s}, C={pkt.c}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: A={pkt.a}, B={pkt.b}. EXPECTED S={self.golden_model.s}, C={self.golden_model.c}. RECEIVED S={pkt.s}, C={pkt.c}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
```

---

## Typical console output (example)
```console
5.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: A=0, B=0 -> S=0, C=0
10.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: A=1, B=0 -> S=1, C=0
15.00ns ERROR    testbench.py(126)[uvm_test_top.env.scoreboard]: FAIL: A=1, B=1. EXPECTED S=0, C=1. RECEIVED S=1, C=0
TEST FAILED: Scoreboard found 1 errors.
```

## Typical console output (placeholder)
```console
get_inst_coverage: False
     2.00ns INFO     ..VM/HalfAdder/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A=1, B=1 -> S=0, C=1
get_inst_coverage: True
     2.00ns INFO     ..VM/HalfAdder/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A=1, B=0 -> S=1, C=0
get_inst_coverage: False
     2.00ns INFO     ..VM/HalfAdder/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A=0, B=1 -> S=1, C=0
get_inst_coverage: False
     2.01ns INFO     ..VM/HalfAdder/MyScoreboard.py(34) [uvm_test_top.env.scoreboard]: TEST PASS: All transactions were correct.
get_inst_coverage: True
     2.01ns INFO     ..yUVM/HalfAdder/MyCoverage.py(23) [uvm_test_top.env.coverage]: Covered all operations (100.00%)
     2.01ns INFO     cocotb.regression                  MyTest.MyTest passed
     2.01ns INFO     cocotb.regression                  **************************************************************************************
                                                        ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        **************************************************************************************
                                                        ** MyTest.MyTest                  PASS           2.01           0.01        164.16  **
                                                        **************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0                  2.01           0.01        159.44  **
                                                        **************************************************************************************
```
## Debugging tips
- Use `PYUVM_LOGLEVEL=DEBUG` for verbose output.
- Re-run failing vectors as directed tests to inspect waveforms.

