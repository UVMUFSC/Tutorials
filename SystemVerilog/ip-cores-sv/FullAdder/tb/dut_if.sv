//------------------------------------------------------------------------------
// DUT interface for the Full Adder testbench.
// Provides a clocked, handshake-based bus for stimulus and observation.
//------------------------------------------------------------------------------
interface dut_if (clk, rst);

    // Clock input from the testbench top.
    input bit clk;
    input logic rst;             // Active-high reset

    // Simple handshake and data buses.
    logic valid_in;          // Driver asserts when inputs are valid
    logic valid_out;         // DUT wrapper asserts when outputs are valid
    logic [2:0] data_bus_in; // [0]=a_i, [1]=b_i, [2]=carry_i
    logic [4:0] data_bus_out;// [0]=a_i, [1]=b_i, [2]=carry_i, [3]=sum_o, [4]=carry_o

endinterface