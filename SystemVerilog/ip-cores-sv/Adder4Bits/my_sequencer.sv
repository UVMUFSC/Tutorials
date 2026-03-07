//------------------------------------------------------------------------------
// UVM sequencer: arbitrates and provides sequence items to the driver.
//------------------------------------------------------------------------------
class my_sequencer extends uvm_sequencer #(pkt);

    `uvm_component_utils (my_sequencer)

	// Standard constructor.
	function new (string name="m_sequencer", uvm_component parent);
		super.new (name, parent);
	endfunction

endclass