//------------------------------------------------------------------------------
// DUT wrapper: connects the DUT to the virtual interface and implements
// a simple valid_in/valid_out handshake plus registered outputs.
//------------------------------------------------------------------------------
module full_adder_wrapper (dut_if vif);

    // Internal DUT outputs.
    logic sum_o, carry_o;

    // Instantiate DUT and map inputs/outputs to the interface.
    full_adder DUT(.a_i(vif.data_bus_in[0]), .b_i(vif.data_bus_in[1]), .carry_i(vif.data_bus_in[2]), .sum_o(sum_o), .carry_o(carry_o));


    // Synchronous interface behavior with reset and handshake.
    always@(posedge vif.clk) begin 
        if(vif.rst) begin
            vif.data_bus_in <= '0;
            vif.data_bus_out <= '0;
            vif.valid_in <= '0;
            vif.valid_out <= '0;
        end  
        // When inputs are valid, capture and expose DUT results.
	    if(vif.valid_in == 1) begin
            vif.data_bus_out[0] <= DUT.a_i;
            vif.data_bus_out[1] <= DUT.b_i;
            vif.data_bus_out[2] <= DUT.carry_i;
            vif.data_bus_out[3] <= DUT.sum_o;
            vif.data_bus_out[4] <= DUT.carry_o;
            vif.valid_out <= '1;
	    end  
        else begin
            vif.valid_out <= '0;
        end
    end

endmodule