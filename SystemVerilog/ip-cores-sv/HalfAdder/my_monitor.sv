//------------------------------------------------------------------------------
// UVM monitor: observes DUT outputs and publishes transactions.
// Captures (a,b,c,s) when valid_out is asserted.
//------------------------------------------------------------------------------
class my_monitor extends uvm_monitor;
  `uvm_component_utils (my_monitor)

  // Virtual interface to sample signals.
  virtual dut_if vif;

  // Analysis port for broadcasting observed packets.
  uvm_analysis_port  #(pkt) mon_analysis_port;

  function new (string name = "my_monitor", uvm_component parent = null);
		super.new (name, parent);
	endfunction

  // Create analysis port and get interface handle.
  virtual function void build_phase (uvm_phase phase);
    super.build_phase (phase);

    mon_analysis_port = new ("mon_analysis_port", this);

   if (! uvm_config_db #(virtual dut_if) :: get (this, "", "vif", vif)) begin
      `uvm_error (get_type_name(), "DUT interface not found")
   end  
  endfunction

  // Sample outputs whenever valid_out rises and send to subscribers.
  virtual task run_phase (uvm_phase phase);
    pkt mon_pkt = pkt::type_id::create("mon_pkt", this);

    super.run_phase(phase);

    forever begin
      @(posedge vif.valid_out);
      mon_pkt.a = vif.data_bus_out[0];
      mon_pkt.b = vif.data_bus_out[1];
      mon_pkt.c = vif.data_bus_out[2];
      mon_pkt.s = vif.data_bus_out[3];

      `uvm_info(get_type_name(), $sformatf("Monitorou A=%0d, B=%0d", mon_pkt.a, mon_pkt.b), UVM_LOW)

      mon_analysis_port.write(mon_pkt);
    end
  endtask

endclass