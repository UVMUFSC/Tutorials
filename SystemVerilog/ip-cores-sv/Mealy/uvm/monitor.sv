//------------------------------------------------------------------------------
// UVM monitor: samples Mealy transactions and publishes them to subscribers.
// Uses one thread for sampling and another to release the driver handshake.
//------------------------------------------------------------------------------
class monitor extends uvm_monitor;
    `uvm_component_utils(monitor)

    // Virtual interface handle and analysis output port.
    virtual dut_if vif;
    uvm_analysis_port #(pkt) mon_analysis_port;
    
    // Event used to synchronize the two monitor threads.
    uvm_event ev_capture_done;

    function new(string name = "monitor", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    virtual function void build_phase(uvm_phase phase);
        super.build_phase(phase);
        mon_analysis_port = new("mon_analysis_port", this);
        ev_capture_done   = new("ev_capture_done");

        if (!uvm_config_db #(virtual dut_if)::get(this, "", "vif", vif)) begin
            `uvm_error(get_type_name(), "DUT interface not found")
        end
    endfunction

    virtual task run_phase(uvm_phase phase);
        super.run_phase(phase);
        
        // Run both monitor threads in parallel.
        fork
            sampling_thread();
            control_thread();
        join
    endtask

    // Sample one complete transaction: input/current state, then next state.
    virtual task sampling_thread();
        pkt mon_pkt;
        forever begin
            // Wait until the driver starts a transaction.
            wait(vif.en == 1'b1);
            
            mon_pkt = pkt::type_id::create("mon_pkt", this);
            
            // Capture pre-edge snapshot.
            mon_pkt.inputs  = vif.mon_cb.data_bus_out[3];
            mon_pkt.state   = vif.mon_cb.data_bus_out[2:1];
            mon_pkt.mealy_o = vif.mon_cb.data_bus_out[0];
            mon_pkt.reset = vif.rst;

            // Move to next clock sample to observe next_state.
            @(vif.mon_cb);

            // Capture post-edge state and publish the transaction.
            mon_pkt.next_state = vif.mon_cb.data_bus_out[2:1];

            `uvm_info(get_type_name(),
                $sformatf("Monitored IN=%0d, STATE=%0b, NEXT=%0b, OUT=%0d, RST=%0d",
                          mon_pkt.inputs, mon_pkt.state, mon_pkt.next_state, mon_pkt.mealy_o, mon_pkt.reset),
                UVM_LOW)
            
            mon_analysis_port.write(mon_pkt);
            
            // Notify control thread that sampling is complete.
            ev_capture_done.trigger();
        end
    endtask

    // Clear enable after sampling to unblock the driver.
    virtual task control_thread();
        forever begin
            ev_capture_done.wait_trigger();       
            vif.en <= 1'b0; 
        end
    endtask

endclass
