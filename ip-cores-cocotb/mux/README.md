# Tutorial: Verifying a 4x1 Multiplexer using UVM.

This tutorial is a practical guide focused on verifying a Verilog *4x1 multiplexer* module. It assumes you have already read the main `README.md` and understand the verification architecture (Driver, Monitor, Scoreboard) we are using.

Our goal here is to detail:
1.  The Verilog module we are testing (DUT).
2.  The specific verification logic for the *4x1 multiplexer*.
3.  How to run the simulation and interpret the results.

## Prerequisites

To follow this tutorial, you will need:
* A Verilog simulator (e.g., Icarus Verilog).
* Python 3.6+.
* Cocotb (`pip install cocotb`).
* GTKWave (optional, for waveform viewing).

## File Structure

We assume the following file structure for the project:
```bash
/project-mux-4x1
│
├── mux4x1.v            # Design Under Test 
├── uvm_mux.py          # UVM testbench 
├── Makefile            
└── dump.fst            # (Generated after simulation) Waveform file
```

## 1. The DUT (Design Under Test): `mux4x1.v`

The *4x1 multiplexer* is a combinational circuit that takes four input signals (`x[3:0]`) and a 2-bit selector (`sel`) and routes one of the inputs to the output (`y`). 

Our goal is to prove that our [4x1 multiplexer](https://github.com/UVMUFSC/IP-Cores/tree/main/ip-cores/mux-4x1) verilog implementation is correct. 

# 2. The Verification Logic: `uvm_mux.py`

Although our testbench has several components (Driver, Monitor), the "intelligence" of the 4x1 multiplexer verification is concentrated in two places:

---

## a) The Reference Model (Scoreboard)

The **Scoreboard** needs to know what the correct result is for any given input.  
We do this by implementing the same selection logic as the multiplexer, but in **Python**.  
This is our *golden model*.

Look at the `ref_model` function inside the `Scoreboard` class:

```python
# 4. Scoreboard
class Scoreboard:
    # ... (other functions) ...
    def ref_model(self, tr: MuxTransaction):
        # This is the 'golden model' logic in Python
        if 0 <= tr.sel <= 3:
            y_expected = tr.x[tr.sel]
        else:
            y_expected = 0  # Invalid selector
        
        # Store the expected result for future comparison
        self.expected_queue.append({
            "inputs": (tr.x, tr.sel),
            "outputs": y_expected
        })
```
## b) The Test Sequence (Test)
Since the 4x1 multiplexer has 4 input bits and 2 selector bits, we use random testing to achieve good coverage across all possible combinations.

This is defined in the mux_random_test function:

```python
# 6. Test
@cocotb.test()
async def mux_random_test(dut):
    env = Environment(dut)

    # 1. We perform random testing for comprehensive coverage
    for _ in range(50):
        x = [random.randint(0, 1) for _ in range(4)]
        sel = random.randint(0, 3)
        tr = MuxTransaction(x=x, sel=sel)
        
        # 2. Tell the Scoreboard what to expect
        env.scoreboard.ref_model(tr)
        
        # 3. Send the inputs to the DUT
        await env.driver.drive(tr)
        
        # 4. Capture the DUT outputs (and trigger the Scoreboard)
        await env.monitor.run()

    # 5. Check if any errors were found
    assert env.scoreboard.errors == 0
```


The test uses random inputs to ensure all possible selection scenarios are tested.

# 3. Running the Verification

To run the simulation, we need a Makefile that tells Cocotb which files to use.

##  Makefile

```makefile
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += mux4x1.v

COCOTB_TEST_MODULES = uvm_mux

TOPLEVEL = mux4x1

include $(shell cocotb-config --makefiles)/Makefile.sim
```

With this file in the folder, just run in the terminal:
```bash
make SIM=icarus WAVES=1
```

This will compile the Verilog, start the simulator, and run the Python testbench. 
```bash
WAVES=1
```
It will be responsible for generating the waveform files in `.fst` format.

# 4. Analyzing the Results

After running `make`, we analyze two artifacts:

## a) Console Output
The console shows the Scoreboard log in real-time. Each [SCOREBOARD PASS] line tells us that, for a given set of inputs, the DUT's output matched our reference model's output.
```console
[SCOREBOARD PASS] Entradas x=(1,1,1,1), sel=0 -> y=1
[SCOREBOARD PASS] Entradas x=(1,0,1,0), sel=2 -> y=1
[SCOREBOARD PASS] Entradas x=(1,0,1,1), sel=3 -> y=1
[SCOREBOARD PASS] Entradas x=(0,1,1,0), sel=3 -> y=0
[SCOREBOARD PASS] Entradas x=(1,0,1,1), sel=0 -> y=1
```
The final message TESTS=1 PASS=1 FAIL=0 confirms that the test completed without errors.

## b) Waveform Analysis (GTKWave)

The `make` command also generated a `dump.fst` file. We can open it in GTKWave for visual analysis:
```bash
gtkwave dump.fst
```


# Waveform Analysis

When loading the `x[3:0]`, `sel`, and `y` signals, we see the following graph:

<img src="wave.png" alt="Block Diagram" width="400px">

---

## Step-by-step Analysis (in sync with our test vectors):

1. **x=(1,1,1,1), sel=0:**  
   All inputs are 1, selector `sel` is 0.  
   Output `y` is 1 (selecting x[0]).  
   ✅ **Correct.**

---

2. **x=(1,0,1,0), sel=2:**  
   Inputs are (1,0,1,0), selector `sel` is 2.  
   Output `y` is 1 (selecting x[2]).  
   ✅ **Correct.**

---

3. **x=(1,0,1,1), sel=3:**  
   Inputs are (1,0,1,1), selector `sel` is 3.  
   Output `y` is 1 (selecting x[3]).  
   ✅ **Correct.**

---

4. **x=(0,1,1,0), sel=3:**  
   Inputs are (0,1,1,0), selector `sel` is 3.  
   Output `y` is 0 (selecting x[3]).  
   ✅ **Correct.**

---

5. **x=(1,0,1,1), sel=0:**  
   Inputs are (1,0,1,1), selector `sel` is 0.  
   Output `y` is 1 (selecting x[0]).  
   ✅ **Correct.**

---

## ✅ Visual Confirmation

The visual analysis confirms that the DUT behaved exactly as a **4x1 multiplexer** should,  
validating the **PASS** results from our Scoreboard.
