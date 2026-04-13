//------------------------------------------------------------------------------
// DUT wrapper: connects the DUT to the virtual interface and implements
// a simple valid_in/valid_out handshake plus registered outputs.
//------------------------------------------------------------------------------
module half_adder_wrapper (dut_if vif);

    // Internal DUT outputs.
    logic c, s;

    // Instantiate DUT and map inputs/outputs to the interface.
    half_adder DUT(.a(vif.data_bus_in[0]), .b(vif.data_bus_in[1]), .c(c), .s(s));


    // Synchronous interface behavior with reset and handshake.
    always@(posedge vif.clk) begin :reset
        if(vif.rst) begin
            vif.data_bus_in <= '0;
            vif.data_bus_out <= '0;
            vif.valid_in <= '0;
            vif.valid_out <= '0;
        end  
        // When inputs are valid, capture and expose DUT results.
	if(vif.valid_in == 1) begin
	    vif.data_bus_out[0] <= DUT.a;
	    vif.data_bus_out[1] <= DUT.b;
	    vif.data_bus_out[2] <= DUT.c;
	    vif.data_bus_out[3] <= DUT.s;
	    vif.valid_out <= '1;
	end  
        else begin
            vif.valid_out <= '0;
        end
    end

endmodule