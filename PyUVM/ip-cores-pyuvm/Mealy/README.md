# Tutorial: Verifying a Mealy FSM using PyUVM

This tutorial explains verification of a Mealy finite-state machine (`mealy_fsm.sv`) using PyUVM. Since Mealy outputs depend on both state and input, tests exercise transitions and output behavior and verify outputs for each (state,input) pair.

## File Structure
```bash
ip-cores-pyuvm/Mealy/
├── mealy_fsm.sv
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
└── MealyWrapper.py
```

## The DUT
`mealy_fsm.sv` produces outputs that depend on the current state and the input.

## Verification Logic
- `MyTest`: instantiates the wrapper (BFM), stores it in `ConfigDB`, and starts the environment and sequences.
- `MyEnv`: creates `MyAgent`, `MyScoreboard`, and `MyCoverage` and wires analysis ports (connect the monitor analysis export to `scoreboard.analysis_export`).
- `MyAgent`: contains `MySequencer`, `MyDriver`, and `MyMonitor`.
  - `MyDriver` obtains the BFM from `ConfigDB` and applies stimulus to the DUT.
  - `MyMonitor` samples DUT/wrapper signals, converts them to `Pkt` transactions and writes them to the analysis ports.
- `MyScoreboard`: receives transactions (via `uvm_tlm_analysis_fifo`), compares DUT outputs and next_state with the stateful `GoldenModel` expectations in `run_phase()`, logs PASS/FAIL per transaction, and reports final result in `check_phase()`.
- `MyCoverage`: samples `pyvsc` covergroups and asserts coverage goals in `report_phase()` when targets are met.

Note: Sequences typically call `env.scoreboard.ref_model(tr)` (or rely on an internal golden model in the scoreboard) to register expectations before the driver applies signals.

## Running the Verification
```bash
cd ip-cores-pyuvm/Mealy
# (optional) activate your virtualenv
source venv_cocotb/bin/activate
make
```

---



### GoldenModel (actual implementation)
This module uses a stateful GoldenModel that consumes inputs and updates internal state; the actual `GoldenModel.py` in this folder is used by `MyScoreboard.py`.

```python
class GoldenModel():
    def __init__(self):
        self.mealy_o=0
        self.next_state=0
        self.current_state=0

    def check(self, packet):
        self.current_state = packet.current_state
        self.mealy_o = 0

        if(packet.rst_i == 0):
            self.next_state = 0
            self.mealy_o = 0
                
        else:
            match packet.current_state:
                case 0:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 0
                case 1:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 2
                case 2:
                    if(packet.mealy_i):
                        self.next_state = 3
                    else:
                        self.next_state = 0
                case 3:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 0
                        self.mealy_o = 1
                case _:
                    self.mealy_o = 0
                    self.next_state = 0


        if (self.mealy_o, self.current_state, self.next_state) == (packet.mealy_o, packet.current_state, packet.next_state):
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
                    f"PASS: CURRENT_STATE={pkt.current_state}, INPUT={pkt.mealy_i}, RST={pkt.rst_i} -> OUTPUT={pkt.mealy_o}, NEXT_STATE={pkt.next_state}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: CURRENT_STATE={pkt.current_state}, INPUT={pkt.mealy_i}, RST={pkt.rst_i}. EXPECTED OUTPUT={self.golden_model.mealy_o}, NEXT_STATE={self.golden_model.next_state}. RECEIVED OUTPUT={pkt.mealy_o}, NEXT_STATE={pkt.next_state}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
```

---

## Typical console output (example)
```bash
# TODO: run the test and paste representative terminal output here
[SCOREBOARD PASS] CURRENT_STATE=0 INPUT=1 RST=1 -> OUTPUT=0 NEXT_STATE=1
[SCOREBOARD FAIL] CURRENT_STATE=3 INPUT=0 RST=1: expected OUTPUT=1 NEXT_STATE=0 actual OUTPUT=0 NEXT_STATE=0
TEST FAIL: Scoreboard found 1 errors.
```

## Typical Console output (placeholder)
```bash
get_inst_coverage: True
  3060.00ns INFO     ../PyUVM/Mealy/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: CURRENT_STATE=01, INPUT=0, RST=1 -> OUTPUT=0, NEXT_STATE=10
get_inst_coverage: True
  3070.00ns INFO     ../PyUVM/Mealy/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: CURRENT_STATE=10, INPUT=1, RST=1 -> OUTPUT=0, NEXT_STATE=11
get_inst_coverage: True
  3080.00ns INFO     ../PyUVM/Mealy/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: CURRENT_STATE=11, INPUT=1, RST=1 -> OUTPUT=0, NEXT_STATE=01
get_inst_coverage: False
  3080.00ns INFO     ../PyUVM/Mealy/MyScoreboard.py(34) [uvm_test_top.env.scoreboard]: TEST PASS: All transactions were correct.
get_inst_coverage: True
  3080.00ns INFO     ..VM/PyUVM/Mealy/MyCoverage.py(30) [uvm_test_top.env.coverage]: Covered all operations (100.00%)
  3080.00ns INFO     cocotb.regression                  MyTest.MyTest passed
  3080.00ns INFO     cocotb.regression                  **************************************************************************************
                                                        ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        **************************************************************************************
                                                        ** MyTest.MyTest                  PASS        3080.00           0.06      50155.92  **
                                                        **************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0               3080.00           0.06      49833.78  **
                                                        **************************************************************************************
```

## Debugging
- Increase logging with `PYUVM_LOGLEVEL=DEBUG` and trace transitions; compare logs with `GoldenModel` expectations.

---
