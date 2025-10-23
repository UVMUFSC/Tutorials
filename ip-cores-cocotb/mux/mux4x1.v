module mux4x1(
	x0_i,
	x1_i,
	x2_i,
	x3_i,
	sel_i,
	y_o
);

input logic x0_i, x1_i, x2_i, x3_i;
input logic [1:0] sel_i;
output logic y_o;

always_comb begin

	case(sel_i)
			2'b00 : y_o = x0_i;
			2'b01 : y_o = x1_i;
			2'b10 : y_o = x2_i;
			2'b11 : y_o = x3_i;
			default: $display("Invalid sel input");
		endcase

end

endmodule