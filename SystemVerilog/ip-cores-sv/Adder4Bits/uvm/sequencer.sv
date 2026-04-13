//------------------------------------------------------------------------------
// UVM sequencer: arbitrates and provides sequence items to the driver.
//------------------------------------------------------------------------------
class sequencer extends uvm_sequencer #(pkt);

    `uvm_component_utils (sequencer)

	// Standard constructor.
	function new (string name="sequencer", uvm_component parent);
		super.new (name, parent);
	endfunction

endclass