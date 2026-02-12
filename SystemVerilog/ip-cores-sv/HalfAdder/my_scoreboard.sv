//------------------------------------------------------------------------------
// Scoreboard: checks DUT outputs against expected Half Adder results.
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
    
	bit expected_s; 
        bit expected_c; 
        
        expected_s = data.a ^ data.b; 
        expected_c = data.a & data.b; 

        if (data.s == expected_s && data.c == expected_c) begin
            `uvm_info ("SCOREBOARD", {$sformatf("PASS: A=%0d, B=%0d -> S=%0d, C=%0d", data.a, data.b, data.s, data.c)}, UVM_LOW)
        end 
        else begin
	    string msg = {"FAIL: A=", $sformatf("%0d", data.a), 
                      ", B=", $sformatf("%0d", data.b), 
                      ". ESPERADO S=", $sformatf("%0d", expected_s), 
                      ", RECEBIDO S=", $sformatf("%0d", data.s)};

            `uvm_error ("SCOREBOARD", msg)
            this.num_errors++; 
        end
	endfunction

    // Report final test status based on error count.
    virtual function void check_phase (uvm_phase phase);
        super.check_phase(phase);
        if (this.num_errors > 0) begin
            `uvm_fatal ("FINAL_RESULT", {$sformatf("TEST FAILED: Scoreboard encontrou %0d erros.", num_errors)})
        end 
        else begin
            `uvm_info ("FINAL_RESULT", "TEST PASS: Todas as transacoes foram corretas.", UVM_NONE)
        end
    endfunction

    virtual task run_phase (uvm_phase phase);
        super.run_phase(phase);
    endtask
endclass