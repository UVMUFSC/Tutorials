# PyUVM Verification Tutorials Collection

This directory contains PyUVM-based verification tutorials that build on top of a Cocotb environment. Each tutorial demonstrates how to verify a specific Verilog/SystemVerilog module using the PyUVM phasing and architecture (sequencer → driver → monitor → scoreboard) and coverage driven testing using `vsc`.

## 📁 Project Structure

```
ip-cores-pyuvm/
│
├── HalfAdder/         # Half-Adder PyUVM tutorial
├── FullAdder/         # Full-Adder PyUVM tutorial
├── Adder4Bits/        # 4-bit Adder PyUVM tutorial
├── Demux/             # 1x4 Demultiplexer PyUVM tutorial
├── Mux/               # 4x1 Multiplexer PyUVM tutorial
├── Mealy/             # Mealy state-machine tutorial
└── Moore/             # Moore state-machine tutorial
```

## 🎯 Tutorial Overview

Each tutorial follows a consistent PyUVM style and typically includes:

- Design Under Test (DUT) — SystemVerilog/Verilog module
- PyUVM testbench components: `MyTest`, `MyEnv`, `MyAgent`, `MyDriver`, `MySequencer`, `MyMonitor`, `MyScoreboard`, and `MyCoverage`
- Golden model implementation (reference model in Python)
- Sequence and transaction (`Pkt`) classes implementing randomization
- Coverage models using `vsc` (covergroups + coverpoints + crosses)
- Wrapper/BFM to interact with the DUT from Python
- `Makefile` to run the simulation via cocotb

## 🔍 Main Differences vs. Cocotb-only Tutorials

- **Coverage-driven testing**: Sequences commonly run until a coverage goal is met (e.g., 100%), rather than a fixed set of vectors.
- **UVM-style phasing and components**: Tests use `pyuvm` classes, `ConfigDB` for configuration handles (BFM, coverage objects), and the objection mechanism for test termination control.
- **Decoupled checking**: The scoreboard consumes transactions from monitors and checks results asynchronously using a Golden Model.
- **Functional coverage focus**: The `vsc` library is used to define covergroups and evaluate coverage; tests assert coverage success in `report_phase()`.

## 🏗️ UVM Architecture

Each PyUVM tutorial implements a UVM-style architecture. The diagram below uses nested boxes to emphasize hierarchy (MyTest > MyEnv > MyAgent), and places the BFM and DUT to the right of the Agent (still inside MyTest). Driver connects to the BFM and BFM to the DUT.

```
+----------------------------------------------------------------------------------+
|                                   MyTest                                         |
|                                                                                  |
|  +--------------------------------------+                                        |
|  |               MyEnv                  |                                        |
|  |  +-------------------------------+   |                                        |
|  |  |         MyAgent               |   |                                        |
|  |  |  +-------------+  +---------+ |   |            +-------------+             |
|  |  |  | Sequencer   |  | Driver  |-+---+----------> |     BFM     |             |
|  |  |  +-----^-------+  +----+----+ |   |            +------+------+             |
|  |  |        |                      |   |                   |                    |
|  |  |  +-----+---+  +------v-----+  |   |                   |                    |
|  |  |  | Sequence|  |  Monitor   |<--------------+          v                    |
|  |  |  |  (Pkt)  |  +------^-----+  |   |        |       +-------+               |
|  |  |  +---------+         |        |   |        +-------+  DUT  |               |
|  |  +----------------------|--------+   |                +-------+               |
|  |   +----------------+    |            |                                        |
|  |   |  Scoreboard    |<---+            |                                        |
|  |   +----------------+    |            |                                        |
|  |   +----------------+    |            |                                        |
|  |   |  Coverage      |<---+            |                                        |
|  |   +----------------+                 |                                        |
|  +--------------------------------------+                                        |
+----------------------------------------------------------------------------------+
```

**Note:** Scoreboard and Coverage connect to the Agent through the Monitor (via analysis ports/TLM). Components use `ConfigDB` to share handles when needed (for example, the BFM wrapper or coverage object).

## 🛠️ Prerequisites

- Python 3.8+
- cocotb
- pyuvm (`pip install pyuvm`)
- vsc (`pip install vsc`) for coverage
- Verilator (recommended) or another cocotb-supported simulator
- GNU Make

## 🚀 Quick Start

1. Activate your cocotb virtual environment (if you have one):

```bash
source venv_cocotb/bin/activate
```

2. Install PyUVM and vsc (if not already installed):

```bash
pip install pyuvm vsc
```

3. Choose a tutorial (e.g., `Mux`):

```bash
cd ip-cores-pyuvm/Mux
```

4. Run the simulation:

```bash
make WAVES=1    # or just `make`
```

5. View waveforms (if generated):

```bash
gtkwave dump.fst
```

## 🔧 Example Makefile

Most tutorials include a Makefile similar to this example:

```makefile
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
WAVES=1
VERILOG_SOURCES += $(PWD)/mux.sv
COCOTB_TOPLEVEL = mux4x1
COCOTB_TEST_MODULES = MyTest
include $(shell cocotb-config --makefiles)/Makefile.sim
```

## 🧪 Typical PyUVM Test Flow

1. HDL is compiled (e.g., Verilator)
2. cocotb imports the Python test module (`MyTest`)
3. PyUVM phasing executes: `build_phase()` builds the env and components, `connect_phase()` links TLM/ports, `run_phase()` starts sequences and stimulus
4. Monitors send transactions to the scoreboard and coverage subscriber
5. When coverage goals are reached and objections are dropped, `report_phase()` emits coverage reports and test pass/fail

## 🧾 Debugging Tips

- Use `PYUVM_LOGLEVEL` to control logging verbosity (e.g., `PYUVM_LOGLEVEL=DEBUG make`).
- If coverage fails, check `MyCoverage.report_phase()` logs and the `vsc` covergroup implementation.
- Ensure `ConfigDB` keys match across components (e.g., storing the BFM and coverage handle in the expected scopes).
- If tests end prematurely, verify objection usage in `run_phase()` (raise/drop correctly).

## 📊 Verification Metrics

- Functional coverage (vsc covergroups)
- Behavioural correctness (Scoreboard vs GoldenModel)
- Assertion of coverage in `report_phase()` (tests generally assert success/failure)

## 🤝 Contributing

Contributions are welcome: bug fixes, new tutorials, improved coverage models, or documentation updates.

## 📝 License

This project is intended for educational purposes. See individual tutorial files for additional licensing notes.

---

Happy Verifying! 🎉
