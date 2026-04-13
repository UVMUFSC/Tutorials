//------------------------------------------------------------------------------
// Scoreboard: checks DUT outputs against expected Mealy FSM results.
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
        bit [1:0] exp_next_state;
        bit       exp_mealy_o = 1'b0;

        if(data.reset) begin
            exp_next_state = 2'b00;
        end
        else begin
            case (data.state)
                2'b00: exp_next_state = data.inputs ? 2'b01 : 2'b00;
                2'b01: exp_next_state = data.inputs ? 2'b01 : 2'b10;
                2'b10: exp_next_state = data.inputs ? 2'b11 : 2'b00;
                2'b11: begin
                    exp_next_state = data.inputs ? 2'b01 : 2'b00;
                    exp_mealy_o = data.inputs ? 1'b0 : 1'b1;
                end
                default: exp_next_state = 2'b00;
            endcase
	end

        if ((data.next_state == exp_next_state) && (data.mealy_o == exp_mealy_o)) begin
            `uvm_info ("SCOREBOARD",
                {$sformatf("PASS: IN=%0d, STATE=%0b -> NEXT=%0b, OUT=%0d",
                           data.inputs, data.state, data.next_state, data.mealy_o)},
                UVM_LOW)
        end
        else begin
            string msg = {"FAIL: IN=", $sformatf("%0d", data.inputs),
                          ", STATE=", $sformatf("%0b", data.state),
                          ". EXPECTED NEXT=", $sformatf("%0b", exp_next_state),
                          ", GOT NEXT=", $sformatf("%0b", data.next_state),
                          ", EXPECTED OUT=", $sformatf("%0d", exp_mealy_o),
                          ", GOT OUT=", $sformatf("%0d", data.mealy_o)};

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
