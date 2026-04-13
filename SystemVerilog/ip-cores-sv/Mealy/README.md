# Tutorial: Verifying a Mealy FSM using SystemVerilog UVM

This tutorial verifies `mealy.sv` using a SystemVerilog UVM testbench organized into `rtl`, `tb`, `uvm`, and `sim` folders.

The environment focuses on transition-level checking for a 4-state Mealy FSM:
- State transitions are validated from `(current_state, input)`.
- Output behavior is validated in the same cycle semantics expected by the Mealy model.
- Functional coverage tracks valid FSM transition pairs until reaching 100%.

## File Structure
```bash
ip-cores-sv/Mealy/
├── rtl/
│   └── mealy.sv
├── tb/
│   ├── dut_if.sv
│   ├── mealy_assertions.sv
│   ├── mealy_wrapper.sv
│   └── tb_top.sv
├── uvm/
│   ├── mealy_pkg.sv
│   ├── pkt.sv
│   ├── mealy_sequence.sv
│   ├── sequencer.sv
│   ├── driver.sv
│   ├── monitor.sv
│   ├── agent.sv
│   ├── coverage.sv
│   ├── scoreboard.sv
│   ├── env.sv
│   └── test.sv
└── sim/
    ├── run.f
    └── Makefile
```

## The DUT
The DUT (`mealy.sv`) is a 4-state FSM (`S0`, `S1`, `S2`, `S3`) with one input bit (`mealy_i`) and one output bit (`mealy_o`).

Transition behavior:
- `S0`: `1 -> S1`, `0 -> S0`
- `S1`: `1 -> S1`, `0 -> S2`
- `S2`: `1 -> S3`, `0 -> S0`
- `S3`: `1 -> S1`, `0 -> S0` and asserts `mealy_o = 1`

Reset behavior:
- Active-low reset inside DUT (`rst_i`), driving state back to `S0`.

To see more details about the RTL design of this module, check the [Mealy FSM RTL Design](https://github.com/UVMUFSC/IP-Cores/tree/main/ip-cores/mealy_fsm).

## Verification Logic
- `tb_top`: instantiates interface and wrapper, drives clock/reset, binds assertions, places `vif` in `uvm_config_db`, and calls `run_test("test")`.
- `mealy_pkg`: central include point for all UVM classes and shared `state_t` enum.
- `env`: creates `agent`, `scoreboard`, and `coverage`, then connects analysis ports.
- `agent`: encapsulates `sequencer`, `driver`, and `monitor`.
- `driver`: drives randomized input transactions and controls the handshake (`en`).
- `monitor`: captures `(input, state, next_state, output, reset)` and publishes `pkt` transactions.
- `scoreboard`: compares observed next-state/output against expected Mealy transition logic.
- `coverage`: samples legal transition bins (`state -> next_state`) and reports coverage status.

## Packet / Sequence Item (`pkt`)
The `pkt` class is the sequence item used across the environment.
- `inputs`: randomized input bit (`mealy_i`).
- `state`: sampled current state.
- `next_state`: sampled state after the next clock.
- `mealy_o`: sampled DUT output.
- `reset`: sampled reset snapshot to handle reset-aware checking in the scoreboard.

### Packet (actual implementation)
```sv
class pkt extends uvm_sequence_item;

  rand bit inputs;

  bit [1:0] state, next_state;
  bit mealy_o;
  bit reset;

  `uvm_object_utils_begin(pkt)
    `uvm_field_int (inputs, UVM_DEFAULT)
    `uvm_field_int (state, UVM_DEFAULT)
    `uvm_field_int (next_state, UVM_DEFAULT)
    `uvm_field_int (mealy_o, UVM_DEFAULT)
    `uvm_field_int (reset, UVM_DEFAULT)
  `uvm_object_utils_end

endclass
```

## Interface and Buses (`dut_if`)
For this FSM verification, the bus organization was intentionally changed to support packet capture across one clock transaction, so the monitor can reconstruct FSM behavior correctly (current state and next state relationship).

The interface exposes one input bit and one packed observation bus:
- `data_bus_in`: carries stimulus bit (`mealy_i`) from driver to DUT.
- `data_bus_out[3:0]`: wrapper exports `[3]=mealy_i`, `[2:1]=state`, `[0]=mealy_o`.
- `en`: handshake signal used by driver/monitor synchronization.
- `drv_cb` and `mon_cb`: clocking blocks for clean sampled/driven timing.

### Why this bus structure changed
- A Mealy checker needs temporal context, not only combinational values.
- The monitor first samples `(input, state, output)` and then, on the next clock sample, captures `next_state`.
- Grouping these fields into one packet gives a deterministic scoreboard comparison based on `(state, input) -> (next_state, output)`.

### Structural changes in wrapper, driver, and monitor
- `mealy_wrapper` is now DUT-focused only: it instantiates the FSM and passes/exports signals, without implementing bus-control logic.
- `driver` uses two explicit tasks:
  - `drive_item`: drives stimulus and asserts `en`.
  - `idle`: keeps interface quiescent when no transaction is available.
- `monitor` uses two parallel threads:
  - `sampling_thread`: captures packet fields and publishes transactions.
  - `control_thread`: handles `en` release logic after capture, unblocking the driver.

This split makes the testbench more modular: protocol/control stays in UVM components, while the wrapper remains a thin DUT adapter.

## Wrapper and Assertions
`mealy_wrapper` instantiates `mealy_fsm` and mirrors internal DUT visibility onto `data_bus_out`, including internal state for monitor/coverage usage.

`tb_top` binds `mealy_assertions.sv` directly onto the DUT instance, enabling assertion-based checking in parallel with scoreboard checking.

## Assertions (actual implementation)
Assertions provide cycle-accurate protocol and behavior checks independent from transaction-level scoreboard logic.

```sv
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

  property p_reset;
    @(posedge clk_i)
    !rst_i |=> (state == S0);
  endproperty

  property p_impossible;
    @(posedge clk_i)
    (state == S0) |=> (state != S2);
  endproperty

  property p_output;
    @(posedge clk_i)
    (state == S3 && !mealy_i) |-> (mealy_o);
  endproperty

  property p_s3;
    @(posedge clk_i)
    (state == S3 && !mealy_i) |=> (state == S0);
  endproperty

  P_RESET: assert property(p_reset)
    else `uvm_error("MEALY_ASSERTIONS", "Reset failed")

  P_IMPOSSIBLE: assert property(p_impossible)
    else `uvm_error("MEALY_ASSERTIONS", "Valid state failed")

  P_OUTPUT: assert property(p_output)
    else `uvm_error("MEALY_ASSERTIONS", "State 3 failed")

  P_S3: assert property(p_s3)
    else `uvm_error("MEALY_ASSERTIONS", "State 3 failed")

endmodule
```

Assertion intent:
- `p_reset`: validates reset recovery to `S0`.
- `p_impossible`: blocks an illegal transition (`S0 -> S2`).
- `p_output`: enforces Mealy output timing in `S3` with input `0` (same-cycle implication).
- `p_s3`: enforces the expected next state after the same condition (`S3` with input `0`).

Together, assertions catch local temporal violations early, while the scoreboard validates full packet behavior.

## Sequence and Coverage Synchronization
The sequence (`mealy_sequence`) runs until coverage reaches 100%:
- Reuses a single packet object with repeated randomization.
- Waits on global event `cov_sampled` after each item.
- Reads `cov_status` from `uvm_config_db` to decide whether to continue.

This keeps generation and coverage sampling synchronized transaction-by-transaction.

## Scoreboard (actual implementation)
```sv
class scoreboard extends uvm_scoreboard;
  `uvm_component_utils (scoreboard)

  uvm_analysis_imp #(pkt, scoreboard) ap_imp;
  int num_errors = 0;

  virtual function void write (pkt data);
    bit [1:0] exp_next_state;
    bit       exp_mealy_o = 1'b0;

    if(data.reset) begin
      exp_next_state = 2'b00;
    end
    else begin
      case (data.state)
        2'b00: exp_next_state = data.inputs ? 2'b01 : 2'b00;
        2'b01: exp_next_state = data.inputs ? 2'b01 : 2'b10;
        2'b10: exp_next_state = data.inputs ? 2'b11 : 2'b00;
        2'b11: begin
          exp_next_state = data.inputs ? 2'b01 : 2'b00;
          exp_mealy_o = data.inputs ? 1'b0 : 1'b1;
        end
        default: exp_next_state = 2'b00;
      endcase
    end

    if ((data.next_state == exp_next_state) && (data.mealy_o == exp_mealy_o)) begin
      `uvm_info ("SCOREBOARD", "PASS", UVM_LOW)
    end
    else begin
      `uvm_error ("SCOREBOARD", "FAIL")
      this.num_errors++;
    end
  endfunction
endclass
```

## Coverage (actual implementation)
Coverage is transition-oriented and only counts legal edges in the FSM transition graph.

```sv
class coverage extends uvm_subscriber #(pkt);
  `uvm_component_utils(coverage)

  pkt tr;

  `define TRANS(s, ns) binsof(cp_state) intersect {s} && binsof(cp_next_state) intersect {ns}

  covergroup cg_mealy;
    option.per_instance = 1;

    cp_state:      coverpoint tr.state;
    cp_next_state: coverpoint tr.next_state;

    cross_transitions: cross cp_state, cp_next_state {
      bins s0_to_s0 = `TRANS(S0, S0);
      bins s0_to_s1 = `TRANS(S0, S1);
      bins s1_to_s1 = `TRANS(S1, S1);
      bins s1_to_s2 = `TRANS(S1, S2);
      bins s2_to_s0 = `TRANS(S2, S0);
      bins s2_to_s3 = `TRANS(S2, S3);
      bins s3_to_s0 = `TRANS(S3, S0);
      bins s3_to_s1 = `TRANS(S3, S1);

      ignore_bins others = cross_transitions with (!(
        (cp_state == S0 && cp_next_state == S0) ||
        (cp_state == S0 && cp_next_state == S1) ||
        (cp_state == S1 && cp_next_state == S1) ||
        (cp_state == S1 && cp_next_state == S2) ||
        (cp_state == S2 && cp_next_state == S0) ||
        (cp_state == S2 && cp_next_state == S3) ||
        (cp_state == S3 && cp_next_state == S0) ||
        (cp_state == S3 && cp_next_state == S1)
      ));
    }
  endgroup

  `undef TRANS
endclass
```

About `ignore_bins others`:
- The cross of 4 states by 4 next-states has 16 theoretical combinations.
- The Mealy DUT allows only 8 legal transitions.
- `ignore_bins` removes the 8 illegal/unreachable transitions from coverage accounting.
- This prevents false coverage gaps and makes 100% mean: all valid FSM edges were observed.

## Running the Verification
```bash
cd ip-cores-sv/Mealy/sim
make run
```

Additional targets:
- `make run_log`: run simulation and save console output to `simulation.log`.
- `make gui`: launch simulation in SimVision GUI.

## Console Output
```console
UVM_INFO @ 0: reporter [RNTST] Running test test...
UVM_INFO @ 0: reporter [UVMTOP] UVM testbench topology:
--------------------------------------------------------------
Name                       Type                    Size  Value
--------------------------------------------------------------
uvm_test_top               test                    -     @2640
  env                      env                     -     @2699
    agent                  agent                   -     @2730
      driver               driver                  -     @3518
        rsp_port           uvm_analysis_port       -     @3617
        seq_item_port      uvm_seq_item_pull_port  -     @3568
      monitor              monitor                 -     @3597
        mon_analysis_port  uvm_analysis_port       -     @3700
      sequencer            sequencer               -     @2881
        rsp_export         uvm_analysis_export     -     @2939
        seq_item_export    uvm_seq_item_pull_imp   -     @3487
        arbitration_queue  array                   0     -    
        lock_queue         array                   0     -    
        num_last_reqs      integral                32    'd1  
        num_last_rsps      integral                32    'd1  
    coverage               coverage                -     @2790
      analysis_imp         uvm_analysis_imp        -     @2839
    scoreboard             scoreboard              -     @2760
      ap_imp               uvm_analysis_imp        -     @3777
--------------------------------------------------------------

UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/monitor.sv(63) @ 30: uvm_test_top.env.agent.monitor [monitor] Monitored IN=0, STATE=0, NEXT=0, OUT=0, RST=1
UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/scoreboard.sv(46) @ 30: uvm_test_top.env.scoreboard [SCOREBOARD] PASS: IN=0, STATE=0 -> NEXT=0, OUT=0
UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/mealy_sequence.sv(30) @ 30: uvm_test_top.env.agent.sequencer@@sequence [SEQ] Status: 20.83%
UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/monitor.sv(63) @ 50: uvm_test_top.env.agent.monitor [monitor] Monitored IN=1, STATE=0, NEXT=0, OUT=0, RST=1
UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/scoreboard.sv(46) @ 50: uvm_test_top.env.scoreboard [SCOREBOARD] PASS: IN=1, STATE=0 -> NEXT=0, OUT=0
.
.
.
UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/mealy_sequence.sv(30) @ 350: uvm_test_top.env.agent.sequencer@@sequence [SEQ] Status: 100.00%
UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/mealy_sequence.sv(32) @ 350: uvm_test_top.env.agent.sequencer@@sequence [SEQ] Total packets sent: 17
UVM_INFO /usr/eda/cadence/xcelium2209/tools/methodology/UVM/CDNS-1.1d/sv/src/base/uvm_objection.svh(1268) @ 350: reporter [TEST_DONE] 'run' phase is ready to proceed to the 'extract' phase
UVM_INFO /home/100000001332321/Documents/UVM_UFSC/Mealy/uvm/scoreboard.sv(68) @ 350: uvm_test_top.env.scoreboard [FINAL_RESULT] TEST PASS: All transactions were correct.

--- UVM Report catcher Summary ---


Number of demoted UVM_FATAL reports  :    0
Number of demoted UVM_ERROR reports  :    0
Number of demoted UVM_WARNING reports:    0
Number of caught UVM_FATAL reports   :    0
Number of caught UVM_ERROR reports   :    0
Number of caught UVM_WARNING reports :    0

--- UVM Report Summary ---

** Report counts by severity
UVM_INFO :   56
UVM_WARNING :    0
UVM_ERROR :    0
UVM_FATAL :    0
** Report counts by id
[FINAL_RESULT]     1
[RNTST]     1
[SCOREBOARD]    17
[SEQ]    18
[TEST_DONE]     1
[UVMTOP]     1
[monitor]    17
Simulation complete via $finish(1) at time 350 NS + 51
```

## Notes
- The simulation file list is in `sim/run.f`.
- If paths in `run.f` are absolute and environment-specific, adjust them to your local workspace paths before running.

## Debugging Tips
- Increase verbosity by changing `VERBOSITY` in `sim/Makefile` (for example, `UVM_HIGH`).
- Use `make gui` and inspect state transitions cycle by cycle.
- Keep assertions enabled together with scoreboard for stronger failure localization.
