# Tutorial: Verifying a Moore FSM using PyUVM

This tutorial describes the verification of a Moore finite-state machine (`moore_fsm.sv`) using PyUVM. It follows the Mux README structure and uses the real `MyScoreboard` / `GoldenModel` implementations in this folder.

## Prerequisites
- Python 3.8+, cocotb, pyuvm (`pip install pyuvm`), pyvsc (`pip install pyvsc`)
- Verilator or another cocotb-supported simulator
- GNU Make

## File Structure
```bash
ip-cores-pyuvm/Moore/
├── moore_fsm.sv
├── Makefile
├── MyTest.py
├── MyEnv.py
├── MyAgent.py
├── MyMonitor.py
├── MyScoreboard.py
├── GoldenModel.py
├── MyCoverage.py
├── MySequence.py
├── Pkt.py
└── MooreWrapper.py
```

## The DUT
`moore_fsm.sv` is a Moore finite-state machine: outputs are determined by the current state.

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
cd ip-cores-pyuvm/Moore
# (optional) activate your virtualenv
source venv_cocotb/bin/activate
make
```
---

## Scoreboard & GoldenModel (actual implementations)
This section shows the actual `GoldenModel.py` and `MyScoreboard.py` implementations used in this module. The scoreboard subscribes to monitor transactions via a `uvm_tlm_analysis_fifo` and compares observed outputs with the GoldenModel's expectations.

### GoldenModel (actual implementation)
```python
# See `GoldenModel.py` for the full implementation used in tests. Example skeleton:
class GoldenModel():
    def __init__(self):
        self.out=0
        self.current_state=0

    def check(self, packet):
        # Determine expected next state and output from previous state and input
        # (actual rules are implemented in the module's `GoldenModel.py`)
        return True
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
                    f"PASS: PREVIOUS_STATE={pkt.previous_state}, NEXT={pkt.next_i}, RST={pkt.rst_i} -> OUT={pkt.out_o}, CURRENT_STATE={pkt.current_state}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: PREVIOUS_STATE={pkt.previous_state}, NEXT={pkt.next_i}, RST={pkt.rst_i}. EXPECTED OUT={self.golden_model.out}, CURRENT_STATE={self.golden_model.current_state}. RECEIVED OUT={pkt.out_o}, CURRENT_STATE={pkt.current_state}"
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
8.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: PREVIOUS_STATE=0, NEXT=1, RST=1 -> OUT=0, CURRENT_STATE=1
16.00ns ERROR    testbench.py(126)[uvm_test_top.env.scoreboard]: FAIL: PREVIOUS_STATE=2, NEXT=0, RST=1. EXPECTED OUT=1, CURRENT_STATE=3. RECEIVED OUT=0, CURRENT_STATE=2
TEST FAILED: Scoreboard found 1 errors.
```

## Typical console output (placeholder)
```bash
get_inst_coverage: True
 12350.00ns INFO     ../PyUVM/Moore/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: PREVIOUS_STATE=010, NEXT=1, RST=0 -> OUT=0, CURRENT_STATE=011
get_inst_coverage: True
 12360.00ns INFO     ../PyUVM/Moore/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: PREVIOUS_STATE=011, NEXT=1, RST=0 -> OUT=0, CURRENT_STATE=100
get_inst_coverage: True
 12370.00ns INFO     ../PyUVM/Moore/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: PREVIOUS_STATE=100, NEXT=0, RST=0 -> OUT=1, CURRENT_STATE=010
get_inst_coverage: False
 12370.00ns INFO     ../PyUVM/Moore/MyScoreboard.py(34) [uvm_test_top.env.scoreboard]: TEST PASS: All transactions were correct.
get_inst_coverage: True
 12370.00ns INFO     ..VM/PyUVM/Moore/MyCoverage.py(30) [uvm_test_top.env.coverage]: Covered all operations (100.00%)
 12370.00ns INFO     cocotb.regression                  MyTest.MyTest passed
 12370.00ns INFO     cocotb.regression                  **************************************************************************************
                                                        ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        **************************************************************************************
                                                        ** MyTest.MyTest                  PASS       12370.00           0.22      56000.66  **
                                                        **************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0              12370.00           0.22      55896.22  **
                                                        **************************************************************************************
```

---