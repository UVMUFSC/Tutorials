//------------------------------------------------------------------------------
// UVM driver: drives Half Adder inputs through the virtual interface.
// Pulls transactions from the sequencer and asserts valid_in.
//------------------------------------------------------------------------------
class my_driver extends uvm_driver #(pkt);
    `uvm_component_utils (my_driver)

    // Virtual interface handle and current request.
    virtual dut_if vif;
    pkt req_pkt;

    function new (string name = "my_driver", uvm_component parent);
        super.new(name, parent);
    endfunction

    // Retrieve the virtual interface from the configuration database.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase(phase);
        if (! uvm_config_db #(virtual dut_if) :: get (this, "", "vif", vif)) begin
        	`uvm_fatal (get_type_name (), "Didn't get handle to virtual interface if_name")
     	end
    endfunction

    // Main driver loop: fetch, drive, complete.
    virtual task run_phase(uvm_phase phase);
        super.run_phase(phase);

	    forever begin
		    seq_item_port.get_next_item(req_pkt);

		    drive_item(req_pkt);

		    seq_item_port.item_done();
	    end
    endtask

    // Drive a single transaction on the interface.
    virtual task drive_item (pkt pkt_item);
	@(posedge vif.clk);
        vif.data_bus_in[0] <= pkt_item.a_i;
        vif.data_bus_in[1] <= pkt_item.b_i;
        vif.data_bus_in[2] <= pkt_item.carry_i;


        // Wait for previous output to be cleared before asserting valid.
        wait(vif.valid_out == '0)
            vif.valid_in <= 1'b1; 

        @(posedge vif.clk);
    
        vif.valid_in <= 1'b0; 
    
   endtask

endclass