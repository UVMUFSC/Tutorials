//------------------------------------------------------------------------------
// Scoreboard: checks DUT outputs against expected Adder4Bits environment results.
// Counts errors and reports final pass/fail in check_phase.
//------------------------------------------------------------------------------
class scoreboard extends uvm_scoreboard;
    `uvm_component_utils (scoreboard)

    // Analysis implementation and error counter.
    uvm_analysis_imp #(pkt, scoreboard) ap_imp;
    int num_errors = 0;

    function new (string name = "scoreboard", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create analysis implementation port.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase);
        ap_imp = new ("ap_imp", this);
    endfunction

    // Compare expected vs observed outputs for each transaction.
    virtual function void write (pkt data);
    
        bit [4:0] temp;   
	    bit [3:0] expected_sum; 
        bit expected_carry;
        bit [3:0] a_i;
        bit [3:0] b_i;

        a_i = data.inputs[7:4];
        b_i = data.inputs[3:0];

        temp = {1'b0, a_i} + {1'b0, b_i};
        expected_sum = temp[3:0];
        expected_carry = temp[4];

        if ((data.s_o == expected_sum) && (data.c_o == expected_carry)) begin
            `uvm_info ("SCOREBOARD", {$sformatf("PASS: A=%0d, B=%0d -> SUM=%0d, CO=%0d", a_i, b_i, data.s_o, data.c_o)}, UVM_LOW)
        end 
        else begin
	    string msg = {"FAIL: A=", $sformatf("%0d", a_i), 
                      ", B=", $sformatf("%0d", b_i),
                      ". EXPECTED SUM=", $sformatf("%0d", expected_sum),
                      ", GOT SUM=", $sformatf("%0d", data.s_o),
                      ", EXPECTED CO=", $sformatf("%0d", expected_carry),
                      ", GOT CO=", $sformatf("%0d", data.c_o)};

            `uvm_error ("SCOREBOARD", msg)
            this.num_errors++; 
        end
	endfunction

    // Report final test status based on error count.
    virtual function void check_phase (uvm_phase phase);
        super.check_phase(phase);
        if (this.num_errors > 0) begin
            `uvm_fatal ("FINAL_RESULT", {$sformatf("TEST FAILED: Scoreboard found %0d errors.", num_errors)})
        end 
        else begin
            `uvm_info ("FINAL_RESULT", "TEST PASS: All transactions were correct.", UVM_NONE)
        end
    endfunction

    virtual task run_phase (uvm_phase phase);
        super.run_phase(phase);
    endtask
endclass