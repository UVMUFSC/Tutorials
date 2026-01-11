/*
    Produced by: Bruno Binelli, Bruno Carboni, Eduardo Zambotto, Julio Cezar;
    Date created - 03/2025;
    Description - Moore Finite State Machine
*/

module moore_fsm(
	clk_i,
	rst_i,
	next_i,
	out_o
);

input logic clk_i, rst_i, next_i;
output logic out_o;

typedef enum logic [2:0] { // Listing all states
        S0_MOORE, 
        S1_MOORE, 
        S2_MOORE, 
        S3_MOORE, 
        S4_MOORE 
} states_moore;
    states_moore state_moore;
	 
	 
always_ff @(posedge clk_i) begin
	if (rst_i) begin
            out_o <= 1'b0;
            state_moore <= S0_MOORE;
        end else begin
            case (state_moore) 
                S0_MOORE: begin
                    out_o <= 1'b0;
                    if (next_i) begin
                        state_moore <= S1_MOORE;
                    end
                end

                S1_MOORE: begin 
                    out_o <= 1'b0;
                    if (!next_i) begin 
                        state_moore <= S2_MOORE;
                    end else begin
                        state_moore <= S1_MOORE;
                    end
                end

                S2_MOORE: begin // 10
                    out_o <= 1'b0;
                    if (next_i) begin // 101
                        state_moore <= S3_MOORE;
                    end else begin
                        state_moore <= S0_MOORE;
                    end
                end

                S3_MOORE: begin 
                    out_o <= 1'b0;
                    if (next_i) begin 
                        state_moore <= S4_MOORE;
                    end else begin
                        state_moore <= S2_MOORE;
                    end
                end

                S4_MOORE: begin 
                    out_o <= 1'b1;
                    if (next_i) begin
                        state_moore <= S1_MOORE;
                    end else begin
                        state_moore <= S2_MOORE;
                    end
                end

                default: begin
                    out_o <= 1'b0;
                    state_moore <= S0_MOORE; 
                end
            endcase
        end
    end	 

endmodule