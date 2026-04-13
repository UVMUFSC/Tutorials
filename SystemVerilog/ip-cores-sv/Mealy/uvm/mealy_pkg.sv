//------------------------------------------------------------------------------
// Package: mealy_pkg
// Central include point for all testbench classes and macros.
//------------------------------------------------------------------------------
package mealy_pkg;
    import uvm_pkg::*;
    `include "uvm_macros.svh"

    typedef enum logic [1:0]{
        S0 = 2'b00,
        S1 = 2'b01,
        S2 = 2'b10,
        S3 = 2'b11
    } state_t;

    `include "pkt.sv"
    `include "sequencer.sv"
    `include "mealy_sequence.sv"
    `include "driver.sv"
    `include "monitor.sv"
    `include "agent.sv"
    `include "coverage.sv"
    `include "scoreboard.sv"
    `include "env.sv"
    `include "test.sv"

endpackage