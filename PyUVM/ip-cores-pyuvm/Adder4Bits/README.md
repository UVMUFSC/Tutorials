# Tutorial: Verifying a 4-bit Adder using PyUVM

This tutorial is a practical guide for verifying `adder_4bits.sv` using a PyUVM testbench built on cocotb. It follows the same structure and level of detail used in the Mux README and uses the actual `MyScoreboard` / `GoldenModel` implementations in this folder.

## File Structure
```bash
ip-cores-pyuvm/Adder4Bits/
├── adder_4bits.sv
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
└── Adder4BitsWrapper.py
```

## The DUT
The 4-bit adder computes sum = (a + b) & 0xF and carry = (a + b) >> 4.

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
cd ip-cores-pyuvm/Adder4Bits
# (optional) activate your virtualenv
source venv_cocotb/bin/activate
make        # add WAVES=1 for waveform output when debugging
```

---

## Scoreboard & GoldenModel (actual implementations)
This module uses the real `GoldenModel.py` and `MyScoreboard.py` found in this folder. The Scoreboard receives transactions via a `uvm_tlm_analysis_fifo` and compares DUT outputs with the GoldenModel in `run_phase()`; final check occurs in `check_phase()`.

### GoldenModel (actual implementation)
```python
class GoldenModel():
    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):

        total_sum=int(packet.a_i) + int(packet.b_i)
        self.s=total_sum & 0xF
        self.c = total_sum >> 4

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
                    f"PASS: A_i={pkt.a_i}, B_i={pkt.b_i} -> S_o={pkt.sum_o}, C_o={pkt.carry_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: A_i={pkt.a_i}, B_i={pkt.b_i}. EXPECTED S_o={self.golden_model.s}, C_o={self.golden_model.c}. RECEIVED S_o={pkt.sum_o}, C_o={pkt.carry_o}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
```

> Note: `MyEnv` connects the monitor analysis port to `scoreboard.analysis_export` in `build_phase()` so the scoreboard receives monitor transactions.

---

## Typical console output (example)
```console
19.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: A_i=1, B_i=2 -> S_o=3, C_o=0
38.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: A_i=7, B_i=8 -> S_o=15, C_o=0
57.00ns ERROR    testbench.py(126)[uvm_test_top.env.scoreboard]: FAIL: A_i=15, B_i=15. EXPECTED S_o=14, C_o=1. RECEIVED S_o=13, C_o=1
TEST FAILED: Scoreboard found 1 errors.
```


---



## Typical console output (placeholder)
```console
get_inst_coverage: True
     3.65ns INFO     ..M/Adder4Bits/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A_i=0101, B_i=0011 -> S_o=1000, C_o=0
get_inst_coverage: True
     3.65ns INFO     ..M/Adder4Bits/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A_i=1010, B_i=0101 -> S_o=1111, C_o=0
get_inst_coverage: True
     3.65ns INFO     ..M/Adder4Bits/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: A_i=0001, B_i=1100 -> S_o=1101, C_o=0
get_inst_coverage: False
     3.65ns INFO     ..M/Adder4Bits/MyScoreboard.py(34) [uvm_test_top.env.scoreboard]: TEST PASS: All transactions were correct.
get_inst_coverage: True
     3.65ns INFO     ..UVM/Adder4Bits/MyCoverage.py(24) [uvm_test_top.env.coverage]: Covered all operations (100.00%)
cg.typename=Adder4BitsCovergroup
TYPE Adder4BitsCovergroup : 100.00%
    CVP cp1 : 100.00%
    CVP cp2 : 100.00%
    CROSS cp1X2 : 100.00%
    INST Adder4BitsCovergroup : 100.00%
        CVP cp1 : 100.00%
        CVP cp2 : 100.00%
        CROSS cp1X2 : 100.00%
     3.65ns INFO     cocotb.regression                  MyTest.MyTest passed
     3.65ns INFO     cocotb.regression                  **************************************************************************************
                                                        ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        **************************************************************************************
                                                        ** MyTest.MyTest                  PASS           3.65           0.29         12.45  **
                                                        **************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0                  3.65           0.29         12.43  **
                                                        **************************************************************************************
```

## Debugging tips
- Use `PYUVM_LOGLEVEL=DEBUG` for verbose logging.
- Reproduce failing vectors with directed tests and inspect `dump.fst` in GTKWave.
- If coverage stalls: check covergroup bins and sequence randomization constraints.
