//------------------------------------------------------------------------------
// Package: half_adder_pkg
// Central include point for all testbench classes and macros.
//------------------------------------------------------------------------------
package half_adder_pkg;
    import uvm_pkg::*;

    `include "uvm_macros.svh"
    `include "pkt.sv"
    `include "my_sequencer.sv"
    `include "my_sequence.sv"
    `include "my_driver.sv"
    `include "my_monitor.sv"
    `include "my_agent.sv"
    `include "my_coverage.sv"
    `include "my_scoreboard.sv"
    `include "my_env.sv"
    `include "my_test.sv"

endpackage