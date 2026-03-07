//------------------------------------------------------------------------------
// Transaction item for Adder4Bits verification environment.
// [7:0] inputs are randomized stimulus bits; s_o and c_o are observed outputs.
//------------------------------------------------------------------------------
class pkt extends uvm_sequence_item;

  // Randomized stimulus inputs.
  randc bit [7:0] inputs;  

  // Observed outputs.
  bit [3:0] s_o;
  bit c_o;

  `uvm_object_utils_begin(pkt)
    `uvm_field_int (inputs, UVM_DEFAULT)
    `uvm_field_int (s_o, UVM_DEFAULT)
    `uvm_field_int (c_o, UVM_DEFAULT)
  `uvm_object_utils_end


  // Initialize outputs to zero.
  function new(string name = "pkt");
      super.new(name);
      this.c_o = '0;
      this.s_o = '0;
  endfunction

endclass