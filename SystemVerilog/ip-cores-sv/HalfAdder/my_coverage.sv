//------------------------------------------------------------------------------
// Coverage collector: samples input space and reports coverage status.
// Uses a global event to notify the sequence that sampling is complete.
//------------------------------------------------------------------------------
class my_coverage extends uvm_subscriber #(pkt);
  `uvm_component_utils(my_coverage)

  // Last observed transaction and sync event.
  pkt tr;
  uvm_event cov_sampled_event;

  // Covergroup for input space (a,b).
  covergroup cg_adder;
    option.per_instance = 1; // per-instance coverage
    cp_a: coverpoint tr.a;
    cp_b: coverpoint tr.b;
    cross_ab: cross cp_a, cp_b;
  endgroup


  // Constructor: build covergroup and get global event handle.
  function new(string name, uvm_component parent);
    super.new(name, parent);
    cg_adder = new();
    cg_adder.set_inst_name("half_adder_cov");
    cov_sampled_event = uvm_event_pool::get_global("cov_sampled");
  endfunction

  // Sample coverage and publish current coverage percentage.
  virtual function void write(pkt t);
    this.tr = t;
    cg_adder.sample();
    uvm_config_db#(real)::set(null, "*", "cov_status", cg_adder.get_inst_coverage());
    cov_sampled_event.trigger();
  endfunction
endclass