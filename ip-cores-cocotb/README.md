# UVM Verification Tutorials Collection

This repository contains a comprehensive collection of UVM (Universal Verification Methodology) tutorials for verifying various digital circuits using Python and Cocotb. Each tutorial demonstrates how to verify a specific Verilog/SystemVerilog module using modern verification techniques.

## 📁 Project Structure

```
uvmzadas/
│
├── half_adder/         # Half-Adder verification tutorial
├── full_adder/         # Full-Adder verification tutorial  
├── adder4bits/         # 4-bit Adder verification tutorial
├── demux/              # 1x4 Demultiplexer verification tutorial
├── mux/                # 4x1 Multiplexer verification tutorial
└── ula/                # Arithmetic Logic Unit verification tutorial
```

## 🎯 Tutorial Overview

Each tutorial follows a consistent structure and covers:

1. **Design Under Test (DUT)** - The Verilog/SystemVerilog module being verified
2. **UVM Testbench** - Python-based verification environment using Cocotb
3. **Reference Model** - Golden model implementation in Python
4. **Test Sequences** - Directed and random testing strategies
5. **Results Analysis** - Console output and waveform interpretation

## 📚 Available Tutorials

### 1. [Half-Adder Tutorial](./half_adder/README.md)
- **Module**: Simple 2-bit adder (a + b = sum + carry)
- **Complexity**: Beginner
- **Testing**: Exhaustive (all 4 combinations)
- **Key Concepts**: Basic UVM architecture, reference model, scoreboard

### 2. [Full-Adder Tutorial](./full_adder/README.md)
- **Module**: 3-bit adder with carry-in (a + b + cin = sum + carry)
- **Complexity**: Beginner
- **Testing**: Directed corner cases + random testing
- **Key Concepts**: Extended UVM patterns, carry propagation

### 3. [4-bit Adder Tutorial](./adder4bits/README.md)
- **Module**: 4-bit arithmetic adder
- **Complexity**: Intermediate
- **Testing**: Corner cases + random testing
- **Key Concepts**: Multi-bit operations, overflow handling

### 4. [1x4 Demultiplexer Tutorial](./demux/README.md)
- **Module**: Signal routing circuit (1 input → 4 outputs)
- **Complexity**: Intermediate
- **Testing**: Random testing
- **Key Concepts**: Signal routing verification, selector logic

### 5. [4x1 Multiplexer Tutorial](./mux/README.md)
- **Module**: Signal selection circuit (4 inputs → 1 output)
- **Complexity**: Intermediate
- **Testing**: Random testing
- **Key Concepts**: Signal selection verification, combinational logic

### 6. [Arithmetic Logic Unit Tutorial](./ula/README.md)
- **Module**: 8-bit ALU with 16 operations
- **Complexity**: Advanced
- **Testing**: Directed + random testing
- **Key Concepts**: Complex operations, multiple opcodes, arithmetic/logic operations

## 🛠️ Prerequisites

To follow these tutorials, you will need:

- **Verilog Simulator**: Icarus Verilog (recommended) or ModelSim
- **Python 3.6+**: For running the testbenches
- **Cocotb**: Python-based verification framework (`pip install cocotb`)
- **GTKWave**: For waveform viewing (optional but recommended)
- **Git**: For version control

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd uvmzadas
   ```

2. **Install dependencies**:
   ```bash
   pip install cocotb
   ```

3. **Choose a tutorial**:
   ```bash
   cd half_adder  # Start with the simplest tutorial
   ```

4. **Run the simulation**:
   ```bash
   make SIM=icarus WAVES=1
   ```

5. **View results**:
   ```bash
   gtkwave dump.fst  # View waveforms
   ```

## 📖 Learning Path

We recommend following the tutorials in this order:

1. **Start with [Half-Adder](./half_adder/README.md)** - Learn basic UVM concepts
2. **Continue with [Full-Adder](./full_adder/README.md)** - Understand carry propagation
3. **Progress to [4-bit Adder](./adder4bits/README.md)** - Multi-bit arithmetic
4. **Explore [Demultiplexer](./demux/README.md)** - Signal routing concepts
5. **Study [Multiplexer](./mux/README.md)** - Signal selection logic
6. **Master [ALU](./ula/README.md)** - Complex multi-operation unit

## 🏗️ UVM Architecture

Each tutorial implements a consistent UVM architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Driver      │    │     Monitor     │    │   Scoreboard    │
│                 │    │                 │    │                 │
│ - Drives DUT    │    │ - Captures      │    │ - Reference     │
│ - Generates     │    │   outputs       │    │   Model         │
│   transactions  │    │ - Triggers      │    │ - Compares      │
│                 │    │   scoreboard    │    │   results       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                         ┌─────────────────┐
                         │       DUT         │
                         │   (Verilog/      │
                         │  SystemVerilog)  │
                         └─────────────────┘
```

## 🧪 Testing Strategies

### Directed Testing
- **Purpose**: Verify specific corner cases and edge conditions
- **Coverage**: Targeted scenarios (e.g., overflow, underflow, boundary values)
- **Example**: Testing all possible input combinations for a half-adder

### Random Testing
- **Purpose**: Achieve broad coverage with minimal test vectors
- **Coverage**: Statistical distribution across input space
- **Example**: Random inputs for complex modules like ALU

### Combined Approach
- **Purpose**: Balance thoroughness with efficiency
- **Coverage**: Directed tests for critical cases + random tests for general coverage
- **Example**: Corner cases + random testing for 4-bit adder

## 📊 Verification Metrics

Each tutorial demonstrates key verification metrics:

- **Functional Coverage**: All operations tested
- **Code Coverage**: All code paths exercised
- **Assertion Coverage**: Design properties verified
- **Regression Testing**: Automated test execution

## 🔍 Results Analysis

### Console Output
- **Scoreboard Logs**: Real-time pass/fail notifications
- **Test Statistics**: Final test results summary
- **Error Reporting**: Detailed failure analysis

### Waveform Analysis
- **Signal Visualization**: GTKWave waveform viewing
- **Timing Analysis**: Signal timing relationships
- **Debugging**: Visual debugging of design issues

## 🤝 Contributing

This tutorial collection is designed to be educational and extensible. Contributions are welcome:

1. **Bug Fixes**: Report and fix issues in existing tutorials
2. **New Tutorials**: Add verification tutorials for additional modules
3. **Improvements**: Enhance existing tutorials with better examples
4. **Documentation**: Improve explanations and add more details

## 📝 License

This project is intended for educational purposes. Please refer to the individual tutorial files for specific licensing information.

## 🙏 Acknowledgments

- **UVMUFSC**: For the IP-Cores repository that inspired these tutorials
- **Cocotb Community**: For the excellent Python-based verification framework
- **Open Source Tools**: Icarus Verilog, GTKWave, and other verification tools

## 📞 Support

For questions or issues:

1. **Check the individual tutorial READMEs** for specific guidance
2. **Review the console output** for error messages
3. **Examine the waveform files** for visual debugging
4. **Consult the Cocotb documentation** for framework-specific issues

---

**Happy Verifying! 🎉**

Start with the [Half-Adder Tutorial](./half_adder/README.md) to begin your UVM verification journey.
