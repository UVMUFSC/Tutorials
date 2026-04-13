//------------------------------------------------------------------------------
// Transaction item for the Mealy FSM verification environment.
// Captures input bit, current state, next state, output, and reset snapshot.
//------------------------------------------------------------------------------
class pkt extends uvm_sequence_item;

  // Randomized stimulus inputs.
  rand bit inputs;  

  // Observed outputs.
  bit [1:0] state, next_state;
  bit mealy_o;
  bit reset;

  `uvm_object_utils_begin(pkt)
    `uvm_field_int (inputs, UVM_DEFAULT)
    `uvm_field_int (state, UVM_DEFAULT)
    `uvm_field_int (next_state, UVM_DEFAULT)
    `uvm_field_int (mealy_o, UVM_DEFAULT)
    `uvm_field_int (reset, UVM_DEFAULT)
  `uvm_object_utils_end


  // Initialize outputs to zero.
  function new(string name = "pkt");
      super.new(name);
      this.state = '0;
      this.next_state = '0;
      this.mealy_o = '0;
      this.reset = '0;
  endfunction

endclass
