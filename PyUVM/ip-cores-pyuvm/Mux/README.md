# Tutorial: Verifying a 4x1 Multiplexer using PyUVM

This tutorial is a practical guide focused on verifying a Verilog *4x1 multiplexer* (`mux4x1.sv`) using a PyUVM testbench. It follows the same structure and level of detail used in the CocoTb examples and uses the actual `MyScoreboard` / `GoldenModel` implementations found in this module.

Our goal here is to detail:
1.  The Verilog module we are testing (DUT).
2.  The verification logic used for the *4x1 multiplexer* (Scoreboard + GoldenModel).
3.  How to run the simulation and interpret the results.

## Prerequisites
To follow this tutorial, you will need:
* Python 3.8+
* cocotb
* pyuvm (`pip install pyuvm`)
* pyvsc (`pip install pyvsc`) if coverage is used
* Verilator or another cocotb-supported simulator
* GTKWave (optional, for waveform viewing)

## File Structure
We assume the following file layout for this module:
```bash
ip-cores-pyuvm/Mux/
├── mux4x1.sv            # Design Under Test
├── Makefile
├── MyTest.py            # Top-level PyUVM test
├── MyEnv.py
├── MyAgent.py
├── MyDriver.py
├── MyMonitor.py
├── MyScoreboard.py      # Scoreboard (PyUVM)
├── GoldenModel.py       # Python GoldenModel
├── MyCoverage.py
├── MySequence.py
├── Pkt.py
└── MyPackage.py
```

## The DUT (Design Under Test): `mux4x1.sv`

The *4x1 multiplexer* is a combinational circuit that takes four input signals (`x0,x1,x2,x3`) and a 2-bit selector (`sel`) and routes the selected input to the output `y`.

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
cd ip-cores-pyuvm/Mux
# (optional) activate virtualenv
source venv_cocotb/bin/activate
make        # add WAVES=1 for waveform output
```

## Scoreboard & GoldenModel (actual implementations)
This folder contains the real `GoldenModel.py` and `MyScoreboard.py` used by the module. The scoreboard receives transactions via a `uvm_tlm_analysis_fifo` and uses the golden model to validate the DUT outputs.

### GoldenModel (actual implementation)
```python
# GoldenModel.py (actual)
class GoldenModel():
    def __init__(self):
        self.y = 0

    def check(self, packet):
        # compute expected y based on sel
        if packet.sel_i == 0:
            self.y = packet.x0_i
        elif packet.sel_i == 1:
            self.y = packet.x1_i
        elif packet.sel_i == 2:
            self.y = packet.x2_i
        else:
            self.y = packet.x3_i

        return packet.y_o == self.y
```

### Scoreboard (actual implementation)
```python
from pyuvm import *
from GoldenModel import GoldenModel

class MyScoreboard(uvm_scoreboard):

    num_errors = 0

    def __init__(self, name, parent):
        super().__init__(name, parent)

    def build_phase(self):
        self.fifo = uvm_tlm_analysis_fifo("fifo", self)
        self.analysis_export = self.fifo.analysis_export
        self.golden_model = GoldenModel()

    async def run_phase(self):
        self.logger.info("Scoreboard starting checks...")
        while True:
            pkt = await self.fifo.get()
            if self.golden_model.check(pkt):
                self.logger.info(
                    f"PASS: X0={pkt.x0_i}, X1={pkt.x1_i}, X2={pkt.x2_i}, X3={pkt.x3_i}, SEL={pkt.sel_i} -> Y={pkt.y_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: X0={pkt.x0_i}, X1={pkt.x1_i}, X2={pkt.x2_i}, X3={pkt.x3_i}, SEL={pkt.sel_i}. EXPECTED Y={self.golden_model.y}. RECEIVED Y={pkt.y_o}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard found {self.num_errors} errors.")
        else:
            self.logger.info("TEST PASS: All transactions were correct.")
```

> Note: `MyEnv` connects the monitor analysis port to `scoreboard.analysis_export` in `build_phase()` so the scoreboard receives monitor transactions.

## Typical console output (example)
```console
19.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: X0=1, X1=0, X2=1, X3=0, SEL=2 -> Y=1
38.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: X0=1, X1=1, X2=1, X3=1, SEL=0 -> Y=1
57.00ns ERROR    testbench.py(126)[uvm_test_top.env.scoreboard]: FAIL: X0=0, X1=1, X2=0, X3=1, SEL=3. EXPECTED Y=0. RECEIVED Y=1
TEST FAILED: Scoreboard found 1 errors.
```

## Typical console output (placeholder)
```console
     2.26ns INFO     ..VM/PyUVM/Mux/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: X0=0, X1=0, X2=1, X3=1, SEL=10 -> Y=1
get_inst_coverage: True
     2.26ns INFO     ..VM/PyUVM/Mux/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: X0=1, X1=0, X2=0, X3=1, SEL=11 -> Y=1
get_inst_coverage: True
     2.26ns INFO     ..VM/PyUVM/Mux/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: X0=1, X1=0, X2=1, X3=0, SEL=10 -> Y=1
get_inst_coverage: False
     2.26ns INFO     ..VM/PyUVM/Mux/MyScoreboard.py(34) [uvm_test_top.env.scoreboard]: TEST PASS: All transactions were correct.
get_inst_coverage: True
     2.26ns INFO     .._UVM/PyUVM/Mux/MyCoverage.py(23) [uvm_test_top.env.coverage]: Covered all operations (100.00%)
     2.26ns INFO     cocotb.regression                  MyTest.MyTest passed
     2.26ns INFO     cocotb.regression                  **************************************************************************************
                                                        ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        **************************************************************************************
                                                        ** MyTest.MyTest                  PASS           2.26           0.08         29.09  **
                                                        **************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0                  2.26           0.08         28.94  **
                                                        **************************************************************************************
```


## Debugging tips
- Use `PYUVM_LOGLEVEL=DEBUG` for verbose testbench messages and trace information.
- Reproduce failing vectors with directed, small tests to step through signals and simplify debugging.
- If the scoreboard never receives transactions, double-check the `monitor` writes and the `analysis_export` connection in `MyEnv.build_phase()`.
- Use `make WAVES=1` and inspect `dump.fst` with GTKWave to debug failing vectors.



