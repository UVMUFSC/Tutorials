//------------------------------------------------------------------------------
// Testbench top: instantiates interface, DUT wrapper, clock/reset, and UVM test.
//------------------------------------------------------------------------------
module tb_top;
    import half_adder_pkg::*;
    import uvm_pkg::*;

    // Clock and reset.
    bit clk;
    bit rst;

    // Virtual interface instance.
    dut_if vif (.clk(clk), .rst(rst));

    // DUT wrapper instance.
    half_adder_wrapper dut(.vif(vif));


    // Free-running clock.
    always #10 clk = ~clk;

    // Reset sequence.
    initial begin
        clk = 0;

        rst = 1;

        #100 rst = 0;
    end

    // UVM configuration and test start.
    initial begin
        uvm_config_db #(virtual dut_if)::set(null, "*", "vif", vif);

        run_test("my_test");
    end    
endmodule