//------------------------------------------------------------------------------
// Package: half_adder_pkg
// Central include point for all testbench classes and macros.
//------------------------------------------------------------------------------
package half_adder_pkg;
    import uvm_pkg::*;

    `include "uvm_macros.svh"
    `include "pkt.sv"
    `include "sequencer.sv"
    `include "halfadder_sequence.sv"
    `include "driver.sv"
    `include "monitor.sv"
    `include "agent.sv"
    `include "coverage.sv"
    `include "scoreboard.sv"
    `include "env.sv"
    `include "test.sv"

endpackage