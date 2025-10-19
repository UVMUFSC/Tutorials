# UVM-Like Tutorial: Principles of Structured Verification

> **📚 Tutorial Relacionado:** Para aprender como configurar o ambiente de desenvolvimento com cocotb, Verilator e GTKWave, consulte o [CocoTb Tutorial](CocoTb_Tutorial.md).

## What is UVM and Structured Verification?

The **Universal Verification Methodology (UVM)** defines a widely adopted, standardized architecture for building scalable and reusable verification environments. While UVM is an official methodology for SystemVerilog, its core concepts—**modularity**, **reusability**, and **separation of concerns**—are fundamental to modern verification in any language, including **cocotb** using Python.

Structured verification aims to separate the **Device Under Test (DUT)** from the code that generates stimulus (inputs) and checks results. This modularity allows complex test scenarios to be built easily and verification components to be reused across different projects.

---

### UVM-Like Testbench Architecture

The architecture organizes the verification components into a **Testbench Hierarchy**, as shown in the diagram:

![UVM Testbench Architecture Diagram](https://github.com/UVMUFSC/Tutorials/blob/main/assets/Block_Diagram.png)

The architecture is typically organized into a top-level **test** module, which manages the **environment (env)**, the **agent**, and the connection to the **interface** and the **DUT**.

---

## Transaction (Sequence Item)

The **Transaction** (or **Sequence Item**) is the fundamental data packet exchanged between verification components. It abstracts low-level signals into meaningful, high-level data.

**Role:** Defines the data structure representing a single operation on the DUT interface (e.g., an input set and expected output).

**Function:** The Transaction class is used to encapsulate meaningful data and control information for a specific operation. Components exchange these high-level objects instead of dealing with individual bits and pins.

**Python Example (`HalfAdderTransaction`):**
```python
@dataclass
class HalfAdderTransaction:
    a: int
    b: int
    s: int = None # Sum (Output)
    c: int = None # Carry (Output)
```
This data class represents a single addition operation, encapsulating both inputs (`a`, `b`) and observed results (`s`, `c`).

---

## Driver

The **Driver** is the active component responsible for taking a high-level transaction and translating it into low-level pin activity on the **interface** of the DUT.

**Role:** Drives stimulus onto the DUT.

**Function:** The Driver receives transactions from the sequencer and converts the high-level data into the corresponding signal toggling required to apply stimulus to the DUT. It acts as a functional model of an external device.

**Python Example (`HalfAdderDriver`):**
```python
class Driver:
    # ... init method ...

    async def drive(self, tr: HalfAdderTransaction):
        # Translate transaction data to DUT signals
        self.dut.a.value = tr.a
        self.dut.b.value = tr.b
        await Timer(10, unit='ns') # Wait for timing/settling
```
---

## Monitor

The **Monitor** is a passive component that observes activity on the DUT interface. It watches the low-level signals and reconstructs them into high-level transactions.

**Role:** Observes interface activity and broadcasts transactions to checking components (like the Scoreboard).

**Function:** The Monitor reads the pin-level signals on the interface and converts this low-level activity back into high-level transaction objects. It then sends these observed transactions to the scoreboard for checking and coverage components for data collection.

**Python Example (`HalfAdderMonitor`):**
```python
class Monitor:
    # ... init method ...

    async def run(self):
        # Wait for outputs to settle (timing is critical in verification!)
        await Timer(9, unit='ns') 
        
        # Read low-level signals and create a high-level transaction
        tr = HalfAdderTransaction(
            a=self.dut.a.value, b=self.dut.b.value,
            s=self.dut.s.value, c=self.dut.c.value
        )
        
        # Send the observed transaction to the Scoreboard
        if self.scoreboard_callback:
            self.scoreboard_callback(tr)
```

---

## Scoreboard

The **Scoreboard** is the verification component responsible for checking the DUT's functional correctness. It is often the most complex component, as it must contain a **Reference Model** (or "golden model").

**Role:** Compares the actual DUT outputs (from the Monitor) with the expected results (from its internal Reference Model).

**Function:**
1.  **Reference Model:** It implements a reference model to calculate the expected output based on the input transactions.
2.  **Checking:** Receives the actual results (from the Monitor) and performs the comparison. 

**Python Example (`HalfAdderScoreboardRefModel`):**
```python
def ref_model(self, tr: HalfAdderTransaction):
    def ref_model(self, tr: HalfAdderTransaction):
        s_expected = tr.a ^ tr.b # XOR for Sum
        c_expected = tr.a & tr.b # AND for Carry
        self.expected_queue.append({  # Queue the expected results..
            "inputs": (tr.a, tr.b),
            "outputs": (s_expected, c_expected)
        })
```

**Python Example (`HalfAdderScoreboardChecking`):**
```python
    def check_actual(self, actual_tr: HalfAdderTransaction):
        if not self.expected_queue:
            print("[SCOREBOARD FAIL] Recebeu um resultado do DUT sem ter um esperado!")
            self.errors += 1
            return

        expected = self.expected_queue.pop(0)
        expected_s, expected_c = expected["outputs"] # Dequeue the expected result
        actual_s, actual_c = actual_tr.s, actual_tr.c

        if expected_s == actual_s and expected_c == actual_c: # Compare with actual_tr.s and actual_tr.c
            print(f"[SCOREBOARD PASS] a={actual_tr.a}, b={actual_tr.b} -> s={actual_s}, c={actual_c}") # ... report PASS/FAIL ...
        else:
            print(f"[SCOREBOARD FAIL] Para a={actual_tr.a}, b={actual_tr.b}:")
            print(f"  -> Esperado: s={expected_s}, c={expected_c}")
            print(f"  -> Recebido: s={actual_s}, c={actual_c}")
            self.errors += 1
```
---

## Environment

The **Environment** is the container that organizes the reusable components (Driver, Monitor, Scoreboard, Agent, etc.). It is responsible for **instantiating** all these pieces and making all the necessary **connections** (like wiring the Monitor's output to the Scoreboard's input).

**Role:** Instantiates, configures, and connects all the lower-level verification components.

**Function:** The Environment ensures that all components that verify a system are correctly instantiated and interconnected, managing the overall configuration of the testbench.

**Python Example (`HalfAdderEnviroment`):**
```python
class Environment:
    def __init__(self, dut):
        self.dut = dut
        self.driver = Driver(dut)
        self.monitor = Monitor(dut)
        self.scoreboard = Scoreboard()
        
        # Connection: Linking Monitor output to Scoreboard input
        self.monitor.scoreboard_callback = self.scoreboard.check_actual
```

---

## Agent (Implicit or Explicit)

The **Agent** groups the components that verify a single interface (Driver, Sequencer, and Monitor).

**Role:** Encapsulates the verification functionality for one specific interface of the DUT.

**Function:** For a simple DUT, the Agent functionality might be **implicit** (managed directly by the Environment). In complex projects, an **explicit Agent** class is essential for reusability, allowing the entire block (Driver, Sequencer, Monitor) to be easily integrated into different environments.

---

## Test

The **Test** class is responsible for setting up the environment, generating test scenarios (sequences of transactions), and reporting the final result.

**Role:** Defines the test scenario and controls the flow of transactions.

**Function:** The Test class configures the environment components (e.g., setting constraints for the stimulus), runs the test flow, and performs the final check of the scoreboard results to determine if the verification passed or failed.

**Python Example (`HalfAdderTest`):**
```python
@cocotb.test()
async def half_adder_uvm_test(dut):
    # 1. Setup Environment
    env = Environment(dut)
    test_vectors = [(0,0), (0,1), (1,0), (1,1)]

    # 2. Stimulus Generation and Verification Loop
    for a, b in test_vectors:
        tr = HalfAdderTransaction(a=a, b=b)
        env.scoreboard.ref_model(tr) # Predict expected result
        await env.driver.drive(tr)   # Drive inputs to DUT
        await env.monitor.run()      # Monitor actual results

    # 3. Final Check
    assert env.scoreboard.errors == 0, f"Scoreboard encontrou {env.scoreboard.errors} erros."
```

---