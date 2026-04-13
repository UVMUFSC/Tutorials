//------------------------------------------------------------------------------
// UVM environment: instantiates agent, scoreboard, and coverage collector.
// Connects monitor analysis port to scoreboard and coverage.
//------------------------------------------------------------------------------
class env extends uvm_env;
    `uvm_component_utils (env)

    // Environment sub-components.
    agent m_agent;
    scoreboard m_scoreboard;
    coverage m_coverage;

    function new (string name = "env", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create environment components.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase);
        m_agent = agent::type_id::create ("agent", this);
        m_scoreboard = scoreboard::type_id::create ("scoreboard", this);
        m_coverage = coverage::type_id::create ("coverage", this);
    endfunction

    // Connect analysis ports to subscribers.
    virtual function void connect_phase (uvm_phase phase);
        super.connect_phase (phase);
        m_agent.m_monitor.mon_analysis_port.connect(m_scoreboard.ap_imp);
        m_agent.m_monitor.mon_analysis_port.connect(m_coverage.analysis_export);
    endfunction

endclass