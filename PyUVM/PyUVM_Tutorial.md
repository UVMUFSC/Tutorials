# PyUVM Setup Guide: UVM Verification with Python

This guide provides the necessary steps to set up a functional environment for **PyUVM**-based verification, extending the cocotb flow with the Universal Verification Methodology (UVM) architecture implemented in Python.

## 📋 Tutorial Scope & Methodology

Before you begin, it is important to understand the **key differences in methodology** between this PyUVM tutorial and the basic cocotb example:

| Aspect | Basic CocoTb Tutorial | PyUVM Tutorial |
| :--- | :--- | :--- |
| **Test Stimulus** | **Pre-defined vectors:** Uses a fixed list of all possible inputs (`[(0,0), (0,1), ...]`). | **Coverage-Driven:** A `Sequence` generates random transactions **until a functional coverage goal is met** (e.g., 100%). |
| **Verification Logic** | **Direct checking:** The test loop immediately checks each result against an expected value. | **Decoupled checking:** The `Scoreboard` compares results asynchronously using a reference model, following the UVM pattern. |
| **Waveform Analysis** | **Encouraged for learning:** Waveforms are shown to trace signal-level behavior for simple, exhaustive tests. | **Not the primary focus:** Due to complex signal hierarchies and random, long-running simulations, analyzing specific waves is less practical. The focus is on **coverage reports and log messages**. |
| **End Condition** | **Fixed-length:** The test ends after processing all vectors in the list. | **Goal-oriented:** The test ends when the coverage monitor reports the target coverage has been achieved. |

**In summary:** This tutorial focuses on building a **professional, scalable verification environment** using UVM principles. You will learn to create a self-checking system that generates intelligent stimulus and uses coverage as a metric for completeness, rather than manually verifying every waveform.

## 1. Prerequisites

Ensure you have completed the **[cocotb Setup Guide](CocoTb_Tutorial.md)** first, as PyUVM builds upon the cocotb infrastructure. You should have:

* **cocotb environment** fully configured (Verilator, GTKWave, Python virtual environment)
* **Python 3.8+** with cocotb installed and working
* **Verilator 5.0+** (or other cocotb-supported simulator)
* **GNU Make** and **C/C++ Compiler**

## 2. Install PyUVM and Dependencies

With your cocotb virtual environment activated, install the additional Python packages required for PyUVM and advanced verification features.

Run these commands in your terminal:

# Activate your existing virtual environment (if not already active)
```bash
source venv_cocotb/bin/activate
```

# Install PyUVM and the Verification Stimulus and Coverage (vsc) library
```bash
pip install pyuvm vsc
```

**Key Packages:**
* **`pyuvm`**: Provides the UVM base classes and phasing system in Python.
* **`vsc`** (Verification Stimulus and Coverage): Enables functional coverage modeling, constraint randomization, and coverage collection.

## 3. Configure the Makefile for PyUVM Tests

Your `Makefile` remains very similar to the standard cocotb one. The key difference is the `MODULE` variable, which should point to your top-level PyUVM test file.

Here's an example Makefile:

# Example Makefile for PyUVM project
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

# === EDIT THESE FOR YOUR PROJECT ===
VERILOG_SOURCES += $(PWD)/rtl/half_adder.v
TOPLEVEL ?= half_adder           # Top module name in your HDL
MODULE ?= tests.test_uvm_half_adder # Python import path to your test
# ===================================

# Enable waveform tracing for GTKWave
VERILATOR_TRACE ?= 1
EXTRA_ARGS += --trace --trace-fst --trace-structs

# Include the standard cocotb Makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

## 4. Run a PyUVM Simulation

The simulation flow is identical to running a standard cocotb test, thanks to the integration between PyUVM and cocotb.

1.  **Navigate to your project directory** (where the `Makefile` is located).
2.  **Run the simulation** (this will compile the HDL and execute the Python testbench):
    
    make
    
    Or, to explicitly enable waveform generation:
    
    make WAVES=1
    
3.  **View waveforms** (if tracing is enabled):
    
    gtkwave dump.fst
    

## 5. Understanding the PyUVM Test Flow

When you execute `make`, the following happens:

1.  **HDL Compilation**: Verilator compiles your RTL code into a simulation model.
2.  **Test Import**: cocotb imports the module specified by `MODULE`.
3.  **PyUVM Phasing**:
    *   The `build_phase()` of all components (`MyEnv`, `MyAgent`, etc.) is called, constructing the testbench hierarchy.
    *   The `connect_phase()` links the components' ports and exports.
    *   The `run_phase()` begins. Your test's `run_phase` (in `MyTest.py`) starts the sequence, which generates and sends transactions via the sequencer-driver-BFM chain to the DUT.
    *   The monitor observes DUT outputs, sends transactions to the scoreboard for checking and to the coverage module for collection.
4.  **Completion**: When the sequence finishes and all objections are dropped, the `report_phase()` is called, displaying coverage results and final pass/fail status.

## 6. Debugging Tips

* **Logging**: PyUVM uses Python's logging module. Control verbosity by setting the `PYUVM_LOGLEVEL` environment variable (e.g., `PYUVM_LOGLEVEL=INFO`, `DEBUG`, `ERROR`).
    
    PYUVM_LOGLEVEL=DEBUG make
    
* **Waveforms**: If a test fails, inspect the `dump.fst` file in GTKWave to debug signal-level issues.
* **Objection Mechanism**: Ensure your test raises and drops objections correctly in the `run_phase()`; otherwise, the simulation may end prematurely.
* **ConfigDB Errors**: A common error is trying to `get()` a configuration handle that was not `set()`. Double-check the path and context in your `build_phase()` methods.

## 7. Further Reading

* **Official PyUVM Documentation**: https://pyuvm.readthedocs.io/
* **vsc (Coverage) Documentation**: https://vsc.readthedocs.io/
---
