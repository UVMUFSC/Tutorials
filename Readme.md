# UVM-Like Tutorial: Principles of Structured Verification

> **📚 Related Tutorial:** To learn how to set up the development environment with cocotb, Verilator and GTKWave, see the [CocoTb Tutorial](CocoTb_Tutorial.md).

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

**CocoTb Example (`HalfAdderTransaction`):**
```python
@dataclass
class HalfAdderTransaction:
    a: int
    b: int
    s: int = None # Sum (Output)
    c: int = None # Carry (Output)
```
**PyUVM Example (`Pkt.py`):**
```python
class Pkt(uvm_sequence_item):
    def __init__(self, name):
        super().__init__(name)
        self.c=0
        self.s=0
        self.a=0
        self.b=0

    def __str__(self):
        return (f"A={self.a}, B={self.b} -> S={self.s}, C={self.c}")
    
    def randomize(self):
        self.a=random.randint(0, 1)
        self.b=random.randint(0, 1)
```
This data class represents a single addition operation, encapsulating both inputs (`a`, `b`) and observed results (`s`, `c`).

---

## Sequence

A **Sequence** defines a series of transactions to be executed.

**Role:** Implements the test stimulus scenarios.

**Function:** It generates `sequence_items` (Transactions), randomizes them, and sends them to the Sequencer. Sequences can implement complex logic, such as waiting for a specific coverage goal before finishing.

**PyUVM Example (`MySequence.py`):**
```python
class MySequence(uvm_sequence):

    def __init__(self, name):
        super().__init__(name)
        self.cov_handle=ConfigDB().get(uvm_root(), "", "COV_HANDLE") # Database configuration so it can access the coverage module

    async def body(self):
        while self.cov_handle.cg.get_coverage() < 100.00: # Creates packages until the coverage is complete (increases the sequence)
            sequence_packet=Pkt.create(f"packet")
            sequence_packet.randomize()
            await Timer(1, unit='step')
            await self.start_item(sequence_packet)
            await self.finish_item(sequence_packet)
```
---

## Sequencer

The **Sequencer** serves as an arbiter that controls the flow of transactions. Inside the `CocoTb` verification, the sequencer is not instantiated, but its function is still present. During the
`PyUVM` verification, the module (`Class`), is identically reconstructed from its parent class `uvm_sequencer`, but it is present in the files to clarify its existence.

**Role:** Manages the communication between Sequences and the Driver.

**Function:** It receives transaction items from sequences and routes them to the driver. In `pyuvm`, it ensures that the driver is ready to process a new item before sending it.

**PyUVM Example (`MySequencer.py`):**
```python
class MySequencer(uvm_sequencer):

    def __init__(self, name, parent):
        super().__init__(name, parent)
```
---

## Driver

The **Driver** is the active component responsible for taking a high-level transaction and translating it into low-level pin activity on the **interface** of the DUT.

**Role:** Drives stimulus onto the DUT.

**Function:** The Driver receives transactions from the sequencer and converts the high-level data into the corresponding signal toggling required to apply stimulus to the DUT. It acts as a functional model of an external device.

**CocoTb Example (`HalfAdderDriver`):**
```python
class Driver:
    # ... init method ...

    async def drive(self, tr: HalfAdderTransaction):
        # Translate transaction data to DUT signals
        self.dut.a.value = tr.a
        self.dut.b.value = tr.b
        await Timer(10, unit='ns') # Wait for timing/settling
```

**PyUVM Example (`MyDriver.py`):**
```python
class MyDriver(uvm_driver):
    # ... init method ...

    def build_phase(self):
        self.bfm = ConfigDB().get(self, "", "BUS_BFM") # Retrieve the BFM handle

    async def run_phase(self):
        while True:
            packet=await self.seq_item_port.get_next_item() # Retrieves another packet from the sequencer (this sequencer port is later defined)
            await self.bfm.send_pkt(packet)
            self.seq_item_port.item_done()
```
---

## Monitor

The **Monitor** is a passive component that observes activity on the DUT interface. It watches the low-level signals and reconstructs them into high-level transactions.

**Role:** Observes interface activity and broadcasts transactions to checking components (like the Scoreboard).

**Function:** The Monitor reads the pin-level signals on the interface and converts this low-level activity back into high-level transaction objects. It then sends these observed transactions to the scoreboard for checking and coverage components for data collection.

**CocoTb Example (`HalfAdderMonitor`):**
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

**PyUVM Example (`MyMonitor.py`):**
```python
class MyMonitor(uvm_monitor):
    # ... init method ...
    
    def build_phase(self):
        self.ap=uvm_analysis_port("ap", self) # Creates and analysis port, use to send packets to the scoreboard and the coverage module
        self.bfm = ConfigDB().get(self, "", "BUS_BFM")

    async def run_phase(self):
        while True:
            result=await self.bfm.get_result()
            self.logger.debug(f"MONITORED {result}")
            packet=Pkt("monitored_packet")
            packet.a=result[0] # Packs the result of the DUT into a packet instance
            packet.b=result[1]
            packet.s=result[2]
            packet.c=result[3]
            self.ap.write(packet) # Sends the packet to the analysis port
```
---

## Agent and ConfigDB

The **Agent** groups the components that verify a single interface (Driver, Sequencer, and Monitor). Like the **Sequencer**, this module may not be explicitly present in the `CocoTb` verification.

**Role:** Encapsulates the verification functionality for one specific interface of the DUT.

**Function:** It manages the instantiation and connection of the Driver, Sequencer, and Monitor.

### uvm_config_db

In `pyuvm`, the `uvm_config_db` (or `ConfigDB`) is used to store and retrieve configuration handles (like the BFM) or component references. This is similar to the SystemVerilog UVM package, providing a centralized way to share data across the verification hierarchy without passing handles manually through every constructor.

**PyUVM Example (`MyAgent.py`):**
```python
class MyAgent(uvm_agent):
    # ... init method ...
        self.sequencer=None
        self.is_active=is_active # An agente can be inactive, meaning it would not send any signal, only monitor them

    def build_phase(self):
        self.sequencer=MySequencer.create("sequencer", self)
        if self.is_active:
            self.driver=MyDriver.create("driver", self)
        self.monitor=MyMonitor.create("monitor", self)

    def connect_phase(self):
        if self.is_active:
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export) # Connects the sequencer port to the driver port
```
---

## BFM (Bus Functional Model) / Wrapper

The **BFM** acts as the functional interface between the verification environment and the hardware signals.

**Role:** Bridges the gap between high-level Python commands and low-level DUT pins.

**Function:** It encapsulates cocotb signal assignments and timing (like RisingEdge) inside asynchronous methods. This allows the rest of the UVM components to remain independent of the specific hardware implementation.

**PyUVM Example (`HalfAdderWrapper.py`):**
```python
class HalfAdderWrapper:
    def __init__(self):
        self.dut = cocotb.top
        self.driver_queue = Queue(maxsize=1)
        self.mon_queue = Queue(maxsize=0) 
        self.ack_event = Event()
        self.stimulus_event = Event()
        self.ack_event.set() 

    async def send_pkt(self, packet):
        await self.ack_event.wait()
        self.ack_event.clear()
        await self.driver_queue.put(packet)

    async def driver_task(self):
        while True:
            packet = await self.driver_queue.get() 
            
            self.dut.a.value = packet.a
            self.dut.b.value = packet.b 
            self.stimulus_event.set()

    async def get_result(self):
        return await self.mon_queue.get()
    
    async def monitor_task(self):
        while True:
            await self.stimulus_event.wait()
            self.stimulus_event.clear()
            
            A_in = self.dut.a.value
            B_in = self.dut.b.value
            S_out = self.dut.s.value
            C_out = self.dut.c.value
            
            self.mon_queue.put_nowait((A_in, B_in, S_out, C_out))
            
            self.ack_event.set()
            
    def start_bfm(self):
        cocotb.start_soon(self.driver_task())
        cocotb.start_soon(self.monitor_task())
```
---


## Scoreboard

The **Scoreboard** is the verification component responsible for checking the DUT's functional correctness. It is often the most complex component, as it must contain a **Reference Model** (or "golden model").

**Role:** Compares the actual DUT outputs (from the Monitor) with the expected results (from its internal Reference Model).

**Function:**
1.  **Reference Model:** It implements a reference model to calculate the expected output based on the input transactions.
2.  **Checking:** Receives the actual results (from the Monitor) and performs the comparison. 

**CocoTb Example (`HalfAdderScoreboardRefModel`):**
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

**CocoTb Example (`HalfAdderScoreboardChecking`):**
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
**PyUVM Example (`GoldenModel.py`):**
```python
class GoldenModel():
    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):
        self.s=packet.a ^ packet.b
        self.c = packet.a & packet.b

        if packet.s == self.s and packet.c == self.c:
            return True
        else:
            return False
```

**PyUVM Example (`MyScoreboard.py`):**
```python
class MyScoreboard(uvm_scoreboard):

    num_errors=0

    # ... init method ...
    
    def build_phase(self):
        self.fifo=uvm_tlm_analysis_fifo("fifo", self) # Instantiates the Scoreboard analysis port
        self.analysis_export=self.fifo.analysis_export # Port that conects to the Monitor
        self.golden_model=GoldenModel()

    async def run_phase(self):
        self.logger.info("Scoreboard iniciando checagem...")
        while True:
            pkt = await self.fifo.get()

            if self.golden_model.check(pkt):
                self.logger.info(
                    f"PASS: A={pkt.a}, B={pkt.b} -> S={pkt.s}, C={pkt.c}")
            else:
                self.num_errors += 1
                self.logger.error(
                    f"FAIL: A={pkt.a}, B={pkt.b}. ESPERADO S={self.golden_model.s}, C={self.golden_model.c}. RECEBIDO S={pkt.s}, C={pkt.c}"
                )

    def check_phase(self):
        if self.num_errors > 0:
            self.logger.fatal(f"TEST FAILED: Scoreboard encontrou {self.num_errors} erros.")
        else:
            self.logger.info("TEST PASS: Todas as transações foram corretas.")
```
---

## Coverage

**Coverage** is used to measure how much of the design functionality has been exercised by the tests.

**Role:** Tracks input combinations and design states to ensure the verification plan is met.

**Function:** Using libraries like `vsc`, we can define covergroups and bins to monitor if all possible scenarios (e.g., all combinations of A and B in a Half Adder) were tested.

**PyUVM Example (`HalfAdderCovergroup.py`):**
```python
@covergroup
class HalfAdderCovergroup():

    def __init__(self):
        self.with_sample(
            a=bit_t(1),
            b=bit_t(1)
        )
        self.cp1 = coverpoint(self.a, bins={
            "a_0" : bin(0), "a_1" : bin(1)
            })
        self.cp2 = coverpoint(self.b, bins={
            "b_o" : bin(0), "b_1" : bin(1)
            })

        self.cp1X2 = cross([self.cp1, self.cp2]) # Cross covers all possibilities: 00, 01, 10, 11
```

**PyUVM Example (`MyCoverage.py`):**
```python
class MyCoverage(uvm_subscriber):
    def build_phase(self):
        self.cg=HalfAdderCovergroup()

    def write(self, pkt):

        self.cg.sample(pkt.a, pkt.b) # Automatically sampled when the Monitor writes at the analysis port (because of the parent class uvm_subscriber)

    def report_phase(self):

        cg_percent = self.cg.get_coverage()

        if cg_percent < 100.0:
            self.logger.error(
                f"Coverage FAIL: {100 - cg_percent:.2f}% uncovered."
            )
            assert False
        else:
            self.logger.info(f"Covered all operations (100.00%)")
            assert True

    def get_my_coverage(self):
        return self.cg.get_coverage()
```
---

## Environment

The **Environment** is the container that organizes the reusable components (Driver, Monitor, Scoreboard, Agent, etc.). It is responsible for **instantiating** all these pieces and making all the necessary **connections** (like wiring the Monitor's output to the Scoreboard's input).

**Role:** Instantiates, configures, and connects all the lower-level verification components.

**Function:** The Environment ensures that all components that verify a system are correctly instantiated and interconnected, managing the overall configuration of the testbench.

**CocoTb Example (`HalfAdderEnviroment`):**
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

**PyUVM Example (`MyEnviroment.py`):**
```python
class MyEnv(uvm_env):
    # ... init method ...
    
    def build_phase(self):
        self.agent=MyAgent.create("agent", self)
        self.scoreboard=MyScoreboard.create("scoreboard", self)
        self.coverage=MyCoverage.create("coverage", self)
        ConfigDB().set(uvm_root(), "", "SEQR", self.agent.sequencer)
        ConfigDB().set(uvm_root(), "", "COV_HANDLE", self.coverage) 

    def connect_phase(self):
        self.agent.monitor.ap.connect(self.scoreboard.analysis_export) # Ports connection
        self.agent.monitor.ap.connect(self.coverage.analysis_export)
```
---

## Test

The **Test** class is responsible for setting up the environment, generating test scenarios (sequences of transactions), and reporting the final result.

**Role:** Defines the test scenario and controls the flow of transactions.

**Function:** The Test class configures the environment components (e.g., setting constraints for the stimulus), runs the test flow, and performs the final check of the scoreboard results to determine if the verification passed or failed.

**CocoTb Example (`HalfAdderTest`):**
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

**PyUVM Example (`MyTest.py`):**
```python
@pyuvm.test()
class MyTest(uvm_test):    
    def build_phase(self):
        self.env=MyEnv.create("env", self)
        self.bfm = HalfAdderWrapper()
        ConfigDB().set(self, "*", "BUS_BFM", self.bfm)
        self.bfm.start_bfm()

    async def run_phase(self):

        self.raise_objection()

        await Timer(2, unit="ns")

        seqr=self.env.agent.sequencer
        seq=MySequence.create("seq") # Note that the Sequence wasn't instantiated anywhere before
        await seq.start(seqr)

        self.drop_objection()
```

---