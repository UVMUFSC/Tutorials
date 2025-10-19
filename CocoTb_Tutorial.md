# cocotb Setup Guide: Verilator and GTKWave Flow

This guide provides the necessary steps to set up a functional environment for cocotb, utilizing **Verilator** as the fast open-source simulator and **GTKWave** as the waveform viewer.

## 1. Prerequisites

Ensure you have the following tools installed and accessible from your terminal:

* **Python 3.8+** (We recommend using a Virtual Environment.)
* **pip** (Python's package installer)
* **GNU Make**
* **C/C++ Compiler** (e.g., GCC/G++)

## 2. Install HDL Tools

You must install a Hardware Description Language (HDL) simulator and a waveform viewer.

### A. Install Verilator (Simulator)

Verilator compiles your Verilog/SystemVerilog code into a fast C++ model.

**On Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install verilator
```

**On macOS (using Homebrew):**
```bash
brew install verilator
```

### B. Install GTKWave (Waveform Viewer)

GTKWave is a standard open-source tool for viewing simulation output files (`.vcd` or `.fst`).

**On Linux (Debian/Ubuntu):**
```bash
sudo apt install gtkwave
```

**On macOS (using Homebrew):**
```bash
brew install --cask gtkwave
```

## 3. Set up the Python Environment

It is highly recommended to use a Python Virtual Environment to keep your dependencies isolated.

1.  **Create Virtual Environment (Optional, but Recommended):**
```bash
    python3 -m venv venv_cocotb
```

2.  **Activate Environment:**
```bash
    source venv_cocotb/bin/activate
```

3.  **Install cocotb:**
    Install the core cocotb library using pip.
```bash
    pip install cocotb
```

## 4. Run a Basic Test

cocotb tests typically rely on a **Makefile** to manage the simulation flow and pass commands to Verilator.

### A. Verilator-Specific Settings (Makefile)

To instruct cocotb to use Verilator and generate waveforms, your project's `Makefile` must include the following variables:

* `SIM ?= verilator` (Specify the simulator)
* `TOPLEVEL ?= your_module_name` (Set the top-level module name from your HDL)
* `TOPLEVEL_LANG ?= verilog` (Set the HDL language)
* `VERILATOR_TRACE ?= 1` (Enable FST tracing for GTKWave)
* `EXTRA_ARGS += --trace --trace-fst --trace-structs` (Trace commands for FST output)
* `MODULE ?= your_test_module` (Set the Python test file/module)

### B. Running the Simulation

Execute the test using the `make` command:
```bash
make
```

This command will compile your HDL using Verilator, run the Python testbench via cocotb, and generate the waveform trace (`dump.fst`).

There may be a problem when generating waves just with using the `Makefile` variables. If that happens, try this:
```bash
make WAVES=1
```

### C. Viewing Waveforms

Open the generated waveform file using GTKWave:
```bash
gtkwave dump.fst
```

Inside GTKWave, select the signals under your top-level DUT to view them.

---

For more advanced configuration, simulator-specific settings, and in-depth documentation, please refer to the official cocotb website.

**Further Reading:**
[cocotb Documentation](https://docs.cocotb.org/en/latest/index.html)