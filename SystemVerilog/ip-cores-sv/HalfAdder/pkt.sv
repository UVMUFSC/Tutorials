//------------------------------------------------------------------------------
// Transaction item: represents Half Adder inputs and outputs.
// a,b are randomized; s,c are observed results.
//------------------------------------------------------------------------------
class pkt extends uvm_sequence_item

  // Randomized stimulus inputs.
  rand bit a;  
  rand bit b; 
  // Observed outputs.
  bit s;
  bit c;

  `uvm_object_utils_begin(pkt)
    `uvm_field_int (a, UVM_DEFAULT)
    `uvm_field_int (b, UVM_DEFAULT)
    `uvm_field_int (s, UVM_DEFAULT)
    `uvm_field_int (c, UVM_DEFAULT)
  `uvm_object_utils_end


  // Initialize outputs to zero.
  function new(string name = "pkt");
      super.new(name);
      this.c = '0;
      this.s = '0;
  endfunction

endclass