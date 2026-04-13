//------------------------------------------------------------------------------
// Package: adder_4bits_pkg
// Central include point for all testbench classes and macros.
//------------------------------------------------------------------------------
package adder_4bits_pkg;
    import uvm_pkg::*;

    `include "uvm_macros.svh"
    `include "pkt.sv"
    `include "sequencer.sv"
    `include "adder4bits_sequence.sv"
    `include "driver.sv"
    `include "monitor.sv"
    `include "agent.sv"
    `include "coverage.sv"
    `include "scoreboard.sv"
    `include "env.sv"
    `include "test.sv"

endpackage