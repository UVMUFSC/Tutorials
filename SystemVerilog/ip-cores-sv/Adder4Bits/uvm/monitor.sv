//------------------------------------------------------------------------------
// UVM monitor: observes DUT outputs and publishes transactions.
// Captures (a,b,s,c) when valid_out is asserted.
//------------------------------------------------------------------------------
class monitor extends uvm_monitor;
  `uvm_component_utils (monitor)

  // Virtual interface to sample signals.
  virtual dut_if vif;

  // Analysis port for broadcasting observed packets.
  uvm_analysis_port  #(pkt) mon_analysis_port;

  function new (string name = "monitor", uvm_component parent = null);
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
      mon_pkt.inputs = vif.data_bus_out[12:5];
      mon_pkt.s_o = vif.data_bus_out[4:1];
      mon_pkt.c_o = vif.data_bus_out[0];

      `uvm_info(get_type_name(), $sformatf("Monitored A=%0d, B=%0d, SUM=%0d, CO=%0d", mon_pkt.inputs[7:4], mon_pkt.inputs[3:0], mon_pkt.s_o, mon_pkt.c_o), UVM_LOW)

      mon_analysis_port.write(mon_pkt);
    end
  endtask

endclass