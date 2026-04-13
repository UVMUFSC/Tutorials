//------------------------------------------------------------------------------
// Testbench top: instantiates interface, DUT wrapper, clock/reset, and UVM test.
//------------------------------------------------------------------------------
module tb_top;
    import mealy_pkg::*;
    import uvm_pkg::*;

    // Clock and reset.
    bit clk;
    bit rst;

    // Virtual interface instance.
    dut_if vif (.clk(clk), .rst(rst));

    // DUT wrapper instance.
    mealy_wrapper dut(.vif(vif));

    // Binding the DUT to the assertions module.
    bind dut.DUT mealy_assertions u_assertions(.clk_i(clk_i), .rst_i(rst_i), .mealy_i(mealy_i), .mealy_o(mealy_o), .state(state), .next_state(next_state));


    // Free-running clock.
    always #10 clk = ~clk;

    // Reset sequence.
    initial begin
        clk = 0;

        rst = 1;

        #55 rst = 0;
    end

    // UVM configuration and test start.
    initial begin
        uvm_config_db #(virtual dut_if)::set(null, "*", "vif", vif);

        run_test("test");
    end    
endmodule
