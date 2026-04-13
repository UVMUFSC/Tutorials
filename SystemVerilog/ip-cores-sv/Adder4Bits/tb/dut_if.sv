//------------------------------------------------------------------------------
// DUT interface for the Adder4Bits testbench.
// Provides a clocked, handshake-based bus for stimulus and observation.
//------------------------------------------------------------------------------
interface dut_if (clk, rst);

    // Clock input from the testbench top.
    input bit clk;
    input logic rst;             // Active-high reset

    // Simple handshake and data buses.
    logic valid_in;           // Driver asserts when inputs are valid
    logic valid_out;          // DUT wrapper asserts when outputs are valid
    logic [7:0] data_bus_in;  // [7:4]=a_i, [3:0]=b_i
    logic [12:0] data_bus_out;// [12:9]=a_i, [8:5]=b_i, [4:1]=s_o, [0]=c_o

endinterface