//------------------------------------------------------------------------------
// Scoreboard: checks DUT outputs against expected Full Adder results.
// Counts errors and reports final pass/fail in check_phase.
//------------------------------------------------------------------------------
class my_scoreboard extends uvm_scoreboard;
    `uvm_component_utils (my_scoreboard)

    // Analysis implementation and error counter.
    uvm_analysis_imp #(pkt, my_scoreboard) ap_imp;
    int num_errors = 0;

    function new (string name = "my_scoreboard", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create analysis implementation port.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase);
        ap_imp = new ("ap_imp", this);
    endfunction

    // Compare expected vs observed outputs for each transaction.
    virtual function void write (pkt data);
    
	bit expected_sum; 
        bit expected_carry; 
        
        expected_sum   = data.a_i ^ data.b_i ^ data.carry_i;
        expected_carry = (data.a_i & data.b_i) |
                         (data.a_i & data.carry_i) |
                         (data.b_i & data.carry_i);

        if ((data.sum_o == expected_sum) && (data.carry_o == expected_carry)) begin
            `uvm_info ("SCOREBOARD", {$sformatf("PASS: A=%0d, B=%0d, CI=%0d -> SUM=%0d, CO=%0d", data.a_i, data.b_i, data.carry_i, data.sum_o, data.carry_o)}, UVM_LOW)
        end 
        else begin
	    string msg = {"FAIL: A=", $sformatf("%0d", data.a_i), 
                      ", B=", $sformatf("%0d", data.b_i),
                      ", CI=", $sformatf("%0d", data.carry_i),
                      ". EXPECTED SUM=", $sformatf("%0d", expected_sum),
                      ", GOT SUM=", $sformatf("%0d", data.sum_o),
                      ", EXPECTED CO=", $sformatf("%0d", expected_carry),
                      ", GOT CO=", $sformatf("%0d", data.carry_o)};

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