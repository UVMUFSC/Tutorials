# Tutorial: Verifying a Full-Adder using PyUVM

This tutorial verifies `full_adder.sv` using a PyUVM testbench with coverage-driven randomization. It follows the same structure and level of detail used in the Mux README and uses the actual `MyScoreboard` / `GoldenModel` implementations in this folder.

## File Structure
```bash
ip-cores-pyuvm/FullAdder/
├── full_adder.sv
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
└── FullAdderWrapper.py
```

## The DUT
Full-adder payload: computes sum and carry for a + b + carry_in.

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
cd ip-cores-pyuvm/FullAdder
# (optional) activate your virtualenv
source venv_cocotb/bin/activate
make        # add WAVES=1 for waveform output
```

---

## Scoreboard & GoldenModel (actual implementations)
This module uses the real `GoldenModel.py` and `MyScoreboard.py` implementations in this folder. The Scoreboard receives monitor transactions via a `uvm_tlm_analysis_fifo` and performs checks in `run_phase()`.

### GoldenModel (actual implementation)
```python
class GoldenModel():
    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):
        self.s=packet.a_i ^ packet.b_i ^ packet.carry_i
        self.c = (packet.a_i & packet.b_i) | (packet.a_i & packet.carry_i) | (packet.b_i & packet.carry_i)

        if packet.sum_o == self.s and packet.carry_o == self.c:
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
                    f"PASS: A_i={pkt.a_i}, B_i={pkt.b_i}, C_i={pkt.carry_i} -> S_o={pkt.sum_o}, C_o={pkt.carry_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: A_i={pkt.a_i}, B_i={pkt.b_i}, C_i={pkt.carry_i}. EXPECTED S_o={self.golden_model.s}, C_o={self.golden_model.c}. RECEIVED S_o={pkt.sum_o}, C_o={pkt.carry_o}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
```

> Note: `MyEnv` connects the monitor analysis port to `scoreboard.analysis_export` so the scoreboard receives monitor transactions.

---

## Typical Console output (example)
```console
10.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: A_i=0, B_i=1, C_i=0 -> S_o=1, C_o=0
20.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: A_i=1, B_i=1, C_i=1 -> S_o=1, C_o=1
30.00ns ERROR    testbench.py(126)[uvm_test_top.env.scoreboard]: FAIL: A_i=1, B_i=1, C_i=0. EXPECTED S_o=0, C_o=1. RECEIVED S_o=1, C_o=0
TEST FAILED: Scoreboard found 1 errors.
```
Notes
- Ensure `env.scoreboard.ref_model(tr)` is called before driving the transaction in the sequence.
- If failures occur, reproduce with a small directed sequence and view waveforms.

## Typical console output (placeholder)
```console
get_inst_coverage: False
     2.01ns INFO     ..VM/FullAdder/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A_i=0, B_i=0, C_i=0 -> S_o=0, C_o=0
get_inst_coverage: True
     2.01ns INFO     ..VM/FullAdder/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A_i=0, B_i=1, C_i=0 -> S_o=1, C_o=0
get_inst_coverage: False
     2.01ns INFO     ..VM/FullAdder/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A_i=1, B_i=1, C_i=1 -> S_o=1, C_o=1
get_inst_coverage: False
     2.01ns INFO     ..VM/FullAdder/MyScoreboard.py(34) [uvm_test_top.env.scoreboard]: TEST PASS: All transactions were correct.
get_inst_coverage: True
     2.01ns INFO     ..yUVM/FullAdder/MyCoverage.py(23) [uvm_test_top.env.coverage]: Covered all operations (100.00%)
     2.01ns INFO     cocotb.regression                  MyTest.MyTest passed
     2.01ns INFO     cocotb.regression                  **************************************************************************************
                                                        ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        **************************************************************************************
                                                        ** MyTest.MyTest                  PASS           2.01           0.02        105.91  **
                                                        **************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0                  2.01           0.02        103.23  **
                                                        **************************************************************************************
```

## Debugging tips
- `PYUVM_LOGLEVEL=DEBUG` for detailed traces.
- Confirm the wrapper/BFM interface and that `ref_model()` is called prior to driving.


