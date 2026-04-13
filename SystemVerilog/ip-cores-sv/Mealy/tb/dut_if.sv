//------------------------------------------------------------------------------
// DUT interface for the Mealy FSM testbench.
// Provides a clocked handshake and compact buses for input/state observation.
//------------------------------------------------------------------------------
interface dut_if (clk, rst);

    // Clock input from the testbench top.
    input bit clk;
    input logic rst;             // Active-high reset

    // Handshake and signal buses.
    logic en;       // High while a transaction is being sampled
    logic data_bus_in;  // mealy_i stimulus bit
    logic [3:0] data_bus_out; // [3]=mealy_i, [2:1]=state, [0]=mealy_o

    clocking drv_cb @(posedge clk);
        default input #1step output #0;
        output data_bus_in;
    endclocking

    clocking mon_cb @(posedge clk);
        default input #1step output #0;
        input data_bus_out;
    endclocking

endinterface
