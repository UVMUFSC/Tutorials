//------------------------------------------------------------------------------
// UVM agent: bundles sequencer, driver, and monitor for the Half Adder.
// Active agents build driver/sequencer; monitor is always built.
//------------------------------------------------------------------------------
class my_agent extends uvm_agent;
    `uvm_component_utils (my_agent)

    // Agent sub-components.
    my_driver drv;
    my_monitor mon;
    my_sequencer seqr;

    function new (string name = "my_agent", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create sub-components based on active/passive mode.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase); 

        if(get_is_active()) begin
            seqr = my_sequencer::type_id::create ("seqr", this);
            drv  = my_driver::type_id::create ("drv", this);
        end

        mon  = my_monitor::type_id::create ("mon", this);

    endfunction

    // Connect sequencer to driver.
    virtual function void connect_phase (uvm_phase phase);
        super.connect_phase(phase);
        if (get_is_active()) begin
            drv.seq_item_port.connect (seqr.seq_item_export);
        end
    endfunction

endclass