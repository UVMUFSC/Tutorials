/*
Designed by: Bruno Binelli, Bruno Carboni, Eduardo Zambotto, Julio Cezar;	
Date: 21/03/25;	
Demultiplexier 1x4 - RTL code.
*/
module demux1x4
(
    x_i,
	 sel_i,
	 y0_o,
	 y1_o,
	 y2_o,
	 y3_o
);
	
	input logic x_i;
	input logic [1:0] sel_i;
	output logic y0_o, y1_o, y2_o, y3_o;
	
	always_comb
	begin
	y0_o = 1'b0;
        y1_o = 1'b0;
        y2_o = 1'b0;
        y3_o = 1'b0;
		
		case(sel_i)
			2'b00 : y0_o = x_i;
			2'b01 : y1_o = x_i;
			2'b10 : y2_o = x_i;
			2'b11 : y3_o = x_i;
		endcase
	end



endmodule