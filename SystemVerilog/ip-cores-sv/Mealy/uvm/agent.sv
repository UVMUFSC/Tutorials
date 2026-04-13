//------------------------------------------------------------------------------
// UVM agent: bundles sequencer, driver, and monitor for the Mealy FSM.
// Active agents build driver/sequencer; monitor is always built.
//------------------------------------------------------------------------------
class agent extends uvm_agent;
    `uvm_component_utils (agent)

    // Agent sub-components.
    driver m_driver;
    monitor m_monitor;
    sequencer m_sequencer;

    function new (string name = "agent", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create sub-components based on active/passive mode.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase); 

        if(get_is_active()) begin
            m_sequencer = sequencer::type_id::create ("sequencer", this);
            m_driver  = driver::type_id::create ("driver", this);
        end

        m_monitor = monitor::type_id::create ("monitor", this);

    endfunction

    // Connect sequencer to driver.
    virtual function void connect_phase (uvm_phase phase);
        super.connect_phase(phase);
        if (get_is_active()) begin
            m_driver.seq_item_port.connect (m_sequencer.seq_item_export);
        end
    endfunction

endclass