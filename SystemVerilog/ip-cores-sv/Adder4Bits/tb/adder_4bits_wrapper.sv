//------------------------------------------------------------------------------
// DUT wrapper: connects the DUT to the virtual interface and implements
// a simple valid_in/valid_out handshake plus registered outputs.
//------------------------------------------------------------------------------
module adder_4bits_wrapper (dut_if vif);

    // Internal DUT outputs.
    logic [3:0] s_o;
    logic c_o;

    // Instantiate DUT and map inputs/outputs to the interface.
    adder_4bits DUT(.a_i(vif.data_bus_in[7:4]), .b_i(vif.data_bus_in[3:0]), .s_o(s_o), .c_o(c_o));


    // Synchronous interface behavior with reset and handshake.
    always@(posedge vif.clk) begin 
        if(vif.rst) begin
            vif.data_bus_out <= '0;
            vif.valid_out <= '0;
        end  
        // When inputs are valid, capture and expose DUT results.
	    else if(vif.valid_in == 1) begin
            vif.data_bus_out[12:9] <= DUT.a_i;
            vif.data_bus_out[8:5] <= DUT.b_i;
            vif.data_bus_out[4:1] <= DUT.s_o;
            vif.data_bus_out[0] <= DUT.c_o;
            vif.valid_out <= '1;
	    end  
        else begin
            vif.valid_out <= '0;
        end
    end

endmodule