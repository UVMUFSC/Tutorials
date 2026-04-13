//------------------------------------------------------------------------------
// Coverage collector: samples Mealy state transitions and reports coverage status.
// Uses a global event to notify the sequence that sampling is complete.
//------------------------------------------------------------------------------
class coverage extends uvm_subscriber #(pkt);
  `uvm_component_utils(coverage)

  // Last observed transaction and sync event.
  pkt tr;
  uvm_event cov_sampled_event;

  // Defines a transaction macro for easier redability; It basically just defines all possible transactions.
  `define TRANS(s, ns) binsof(cp_state) intersect {s} && binsof(cp_next_state) intersect {ns}


  // Covergroup for current packet FSM transition space (state -> next_state).
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

      // Defines the ignore bins; Applies the same logic used for the valid bins, but negates it (!).
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

    // Constructor: build covergroup and get global event handle.
  function new(string name = "coverage", uvm_component parent);
    super.new(name, parent);
    cg_mealy = new();
    cg_mealy.set_inst_name("mealy_cov");
    cov_sampled_event = uvm_event_pool::get_global("cov_sampled");
  endfunction

  // Sample coverage and publish current coverage percentage.
  virtual function void write(pkt t);
    this.tr = t;
    cg_mealy.sample();
    uvm_config_db#(real)::set(null, "*", "cov_status", cg_mealy.get_inst_coverage());
    cov_sampled_event.trigger();
  endfunction
endclass
