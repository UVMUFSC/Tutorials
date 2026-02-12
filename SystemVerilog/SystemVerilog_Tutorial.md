
# SystemVerilog UVM Setup Guide: Xcelium Flow

This guide provides the steps to run a **SystemVerilog UVM** verification tutorial using **Xcelium**. The structure follows the same pattern as the **cocotb** and **PyUVM** guides, while explaining key UVM concepts in SV.

## 📋 Tutorial Scope & Methodology

Before you begin, it is useful to understand how this UVM tutorial differs from a basic SV testbench:

| Aspect | Simple SV Testbench | UVM Tutorial (this guide) |
| :--- | :--- | :--- |
| **Test Stimulus** | **Fixed vectors:** manual, limited input sets. | **Coverage-driven:** sequences randomize transactions until the coverage goal is met. |
| **Verification Logic** | **Inline checking:** immediate checks in the same process. | **Decoupled checking:** scoreboard receives transactions asynchronously. |
| **Waveform Analysis** | **Primary focus:** inspect signals to validate behavior. | **Supportive focus:** logs and coverage are primary; waves are used for debug. |
| **End Condition** | **Fixed-length:** ends after a known loop completes. | **Goal-oriented:** ends when coverage reaches the target. |

**In summary:** the goal is to build a scalable, reusable UVM environment with randomized stimulus, coverage-driven completion, and a self-checking scoreboard.

## 1. Prerequisites

Make sure you have access to:

* **Xcelium (xrun)**
* A valid **Cadence license** and environment variables configured
* Basic SystemVerilog knowledge
* If you don't have access to Cadence tools, you can use EDA Playground, but with some limitations

## 2. Environment Notes (VM vs EDA Playground)

* **Current environment**: we are using a **virtual machine already configured with Xcelium**. This guide assumes the Cadence toolchain is installed and ready.
* **EDA Playground**: you can try limited experiments there, but expect **constraints** (simulation time, GUI features, partial UVM support, and licensing restrictions). This tutorial is **focused on the Cadence flow**.

## 3. Configure the Filelist and Project Files

The **Makefile** already cointains the commands needed to run the simulation using Xcelium. It basically indicates the tool that you are using UVM with coverage, and indicates it to clean the coverage files so new coverage data is stored every time the **make** command is used.

The file [run.f](SystemVerilog/ip-cores-sv/HalfAdder/run.f) contains **path placeholders**. Update it with your local paths:

* `-incdir` for includes (for example, your UVM include folder if needed)
* paths for **pkg**, **interface**, **DUT**, **wrapper**, and **tb_top**

> **Note**: in the VM, `-uvm` typically provides the default UVM. If `uvm_macros.svh` is not found, adjust the include path.

## 4. Run the Simulation

1. **Navigate to the UVM files folder** (where the Makefile lives).
2. **Run the simulation**:
	 ```bash
	 make
	 ```
3. **Clean artifacts**:
	 ```bash
	 make clean
	 ```

4. **Run with SimVision (Optional)**:
    ```bash
    make gui
    ```

In SimVision you can acsess lot of options to debug a UVM testbench, like inspecting the UVM components tree (hierarchy), the transactions, running the simulation through UVM phases, and more.

## 5. Understanding the UVM Test Flow

When you run `make`, the following happens:

1. **Compilation**: Xcelium compiles the RTL and testbench files in the order specified by `run.f`.
2. **Build**: `build_phase()` constructs the environment (agent, sequencer, driver, monitor, scoreboard, coverage).
3. **Connections**: `connect_phase()` links analysis ports and sequencer/driver TLM connections.
4. **Stimulus**: the sequence generates randomized transactions and sends them through the sequencer-driver path.
5. **Observation**: the monitor publishes transactions via analysis ports.
6. **Checking & Coverage**: the scoreboard validates results, and coverage updates the goal status.
7. **Completion**: when coverage reaches the target, objections are dropped and the test ends.

The simulation runs through the called UVM phases, wich will be discussed in the next tutorial.

## 6. Debugging Tips

* **Topology print**: `uvm_top.print_topology()` is called in `end_of_elaboration_phase`.
* **Logs**: `uvm_info` and `uvm_error` messages trace the flow and failures.
* **ConfigDB issues**: a common error is calling `get()` without a matching `set()`.
* **GUI debug**: use `-gui` to explore UVM hierarchy and waveforms in SimVision.
* **Coverage status**: verify that the coverage collector updates the goal status.

## 7. Further Reading

* **Accellera UVM Resources**: https://accellera.org
* **IEEE 1800 SystemVerilog Standard**: https://ieeexplore.ieee.org/document/8299595
* **ChipVerify**: https://www.chipverify.com/
---




