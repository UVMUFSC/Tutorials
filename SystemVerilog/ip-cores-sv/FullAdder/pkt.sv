//------------------------------------------------------------------------------
// Transaction item: represents Full Adder inputs and outputs.
// a_i,b_i,carry_i are randomized; sum_o,carry_o are observed results.
//------------------------------------------------------------------------------
class pkt extends uvm_sequence_item;

  // Randomized stimulus inputs.
  rand bit a_i;  
  rand bit b_i; 
  rand bit carry_i;
  // Observed outputs.
  bit sum_o;
  bit carry_o;

  `uvm_object_utils_begin(pkt)
    `uvm_field_int (a_i, UVM_DEFAULT)
    `uvm_field_int (b_i, UVM_DEFAULT)
    `uvm_field_int (carry_i, UVM_DEFAULT)
    `uvm_field_int (sum_o, UVM_DEFAULT)
    `uvm_field_int (carry_o, UVM_DEFAULT)
  `uvm_object_utils_end


  // Initialize outputs to zero.
  function new(string name = "pkt");
      super.new(name);
      this.carry_o = '0;
      this.sum_o = '0;
  endfunction

endclass