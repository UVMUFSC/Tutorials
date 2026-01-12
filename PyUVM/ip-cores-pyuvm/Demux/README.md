# Tutorial: Verifying a 1x4 Demultiplexer (Demux) using PyUVM

This tutorial verifies `demux.sv` with a PyUVM testbench and includes an explicit Scoreboard and GoldenModel example for clarity.

## Goals
- Validate that input `x` is routed to the correct `y[i]` according to selector `sel`.
- Reach coverage targets for selector values and selected input conditions.

## File Structure
```bash
ip-cores-pyuvm/Demux/
├── demux.sv
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
└── DemuxWrapper.py
```

## The DUT
The 1x4 demultiplexer routes `x` to the selected `y[i]` based on `sel`.

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
cd ip-cores-pyuvm/Demux
# (optional) activate your virtualenv
source venv_cocotb/bin/activate
make
```

---

## Scoreboard & GoldenModel (actual implementations)
The `GoldenModel.py` and `MyScoreboard.py` implement the demultiplexing reference model and a scoreboard that reports PASS/FAIL per transaction.

### GoldenModel (actual implementation)
```python
class GoldenModel():
    def __init__(self):
        self.y0=0
        self.y1=0
        self.y2=0
        self.y3=0

    def check(self, packet):
        match packet.sel_i:

            case 0:
                self.y0 = packet.x_i
                self.y1 = 0
                self.y2 = 0
                self.y3 = 0
            case 1:
                self.y1 = packet.x_i
                self.y0 = 0
                self.y2 = 0
                self.y3 = 0
            case 2:
                self.y2 = packet.x_i
                self.y1 = 0
                self.y0 = 0
                self.y3 = 0
            case 3:
                self.y3 = packet.x_i
                self.y1 = 0
                self.y2 = 0
                self.y0 = 0
            

        if (packet.y0_o, packet.y1_o, packet.y2_o, packet.y3_o) == (self.y0, self.y1, self.y2, self.y3):
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
                    f"PASS: X={pkt.x_i}, SEL={pkt.sel_i} -> Y0={pkt.y0_o}, Y1={pkt.y1_o}, Y2={pkt.y2_o}, Y3={pkt.y3_o}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: X={pkt.x_i}, SEL={pkt.sel_i}. EXPECTED Y0={self.golden_model.y0}, Y1={self.golden_model.y1}, Y2={self.golden_model.y2}, Y3={self.golden_model.y3}. RECEIVED Y0={pkt.y0_o}, Y1={pkt.y1_o}, Y2={pkt.y2_o}, Y3={pkt.y3_o}"
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
12.00ns INFO     testbench.py(123)[uvm_test_top.env.scoreboard]: PASS: X=1, SEL=2 -> Y0=0, Y1=0, Y2=1, Y3=0
24.00ns ERROR    testbench.py(126)[uvm_test_top.env.scoreboard]: FAIL: X=1, SEL=3. EXPECTED Y0=0, Y1=0, Y2=0, Y3=1. RECEIVED Y0=0, Y1=0, Y2=0, Y3=0
TEST FAILED: Scoreboard found 1 errors.
```

## Typical console output (placeholder)
```bash
     2.01ns INFO     ../PyUVM/Demux/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: X=0, SEL=10 -> Y0=0, Y1=0, Y2=0, Y3=0
get_inst_coverage: True
     2.02ns INFO     ../PyUVM/Demux/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: X=0, SEL=10 -> Y0=0, Y1=0, Y2=0, Y3=0
get_inst_coverage: True
     2.02ns INFO     ../PyUVM/Demux/MyScoreboard.py(22) [uvm_test_top.env.scoreboard]: PASS: X=1, SEL=01 -> Y0=0, Y1=1, Y2=0, Y3=0
get_inst_coverage: False
     2.02ns INFO     ../PyUVM/Demux/MyScoreboard.py(34) [uvm_test_top.env.scoreboard]: TEST PASS: All transactions were correct.
get_inst_coverage: True
     2.02ns INFO     ..VM/PyUVM/Demux/MyCoverage.py(23) [uvm_test_top.env.coverage]: Covered all operations (100.00%)
     2.02ns INFO     cocotb.regression                  MyTest.MyTest passed
     2.02ns INFO     cocotb.regression                  **************************************************************************************
                                                        ** TEST                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        **************************************************************************************
                                                        ** MyTest.MyTest                  PASS           2.02           0.02        120.67  **
                                                        **************************************************************************************
                                                        ** TESTS=1 PASS=1 FAIL=0 SKIP=0                  2.02           0.02        118.23  **
                                                        **************************************************************************************
```

## Debugging tips
- Use `PYUVM_LOGLEVEL=DEBUG` and reproduce failing vectors with directed tests and GTKWave.

---
