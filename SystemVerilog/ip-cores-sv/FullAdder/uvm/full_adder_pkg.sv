//------------------------------------------------------------------------------
// Package: full_adder_pkg
// Central include point for all testbench classes and macros.
//------------------------------------------------------------------------------
package full_adder_pkg;
    import uvm_pkg::*;

    `include "uvm_macros.svh"
    `include "pkt.sv"
    `include "sequencer.sv"
    `include "fulladder_sequence.sv"
    `include "driver.sv"
    `include "monitor.sv"
    `include "agent.sv"
    `include "coverage.sv"
    `include "scoreboard.sv"
    `include "env.sv"
    `include "test.sv"

endpackage