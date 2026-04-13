//------------------------------------------------------------------------------
// Assertion module for the Mealy FSM.
// Checks reset behavior, forbidden transitions, output condition, and S3 exit.
//------------------------------------------------------------------------------
import mealy_pkg::*;
import uvm_pkg::*;
`include "uvm_macros.svh"


module mealy_assertions (
    clk_i,
    rst_i,
    mealy_i,
    mealy_o,
    state,
    next_state
);

    input logic clk_i, rst_i, mealy_i, mealy_o;
    input logic [1:0] state, next_state;

    // On reset assertion (active-low reset), state must go to S0 on next cycle.
    property p_reset;
        @(posedge clk_i)
        !rst_i |=> (state == S0);
    endproperty

    // From S0, FSM must never jump directly to S2 in the next cycle.
    property p_impossible;
        @(posedge clk_i)
        (state == S0) |=> (state != S2);
    endproperty

    // In S3 with input 0, output must assert in the same cycle (Mealy behavior).
    property p_output;
        @(posedge clk_i)
        (state == S3 && !mealy_i) |-> (mealy_o);
    endproperty

    // In S3 with input 0, next sampled state must be S0.
    property p_s3;
        @(posedge clk_i)
        (state == S3 && !mealy_i) |=> (state == S0);
    endproperty

    // Assertion instances with UVM error reporting.
    P_RESET: assert property(p_reset) 
        else `uvm_error("MEALY_ASSERTIONS", "Reset failed")

    P_IMPOSSIBLE: assert property(p_impossible) 
        else `uvm_error("MEALY_ASSERTIONS", "Valid state failed")

    P_OUTPUT: assert property(p_output) 
        else `uvm_error("MEALY_ASSERTIONS", "State 3 failed")

    P_S3: assert property(p_s3) 
        else `uvm_error("MEALY_ASSERTIONS", "State 3 failed")

endmodule
