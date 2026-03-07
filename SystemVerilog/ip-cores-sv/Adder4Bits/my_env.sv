//------------------------------------------------------------------------------
// UVM environment: instantiates agent, scoreboard, and coverage collector.
// Connects monitor analysis port to scoreboard and coverage.
//------------------------------------------------------------------------------
class my_env extends uvm_env;
    `uvm_component_utils (my_env)

    // Environment sub-components.
    my_agent agent;
    my_scoreboard scoreboard;
    my_coverage coverage;

    function new (string name = "my_env", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create environment components.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase);
        agent = my_agent::type_id::create ("agent", this);
        scoreboard = my_scoreboard::type_id::create ("scoreboard", this);
        coverage = my_coverage::type_id::create ("coverage", this);
    endfunction

    // Connect analysis ports to subscribers.
    virtual function void connect_phase (uvm_phase phase);
        super.connect_phase (phase);
        agent.mon.mon_analysis_port.connect(scoreboard.ap_imp);
        agent.mon.mon_analysis_port.connect(coverage.analysis_export);
    endfunction

endclass