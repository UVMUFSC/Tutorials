/*
	Produced by: Bruno Binelli, Bruno Carboni, Eduardo Zambotto, Julio Cezar;
	Date created - 03/2025;
	Description - Melay Finite State Machine with a 2-bit state register.
*/

/*
 States transition logic:
	{current_state}
		({input}, {output}) -> {next_state}
				     			. . .
	S0:
	    (0,0) -> S0
		(1,0) -> S1
	S1:
		(0,0) -> S2
		(1,0) -> S1
	S2:
		(0,0) -> S0
		(1,0) -> S3
	S3:
		(0,1) -> S0
		(1,0) -> S1
*/

module mealy_fsm(
	clk_i,
	rst_i,
	mealy_i,
	mealy_o
);

input clk_i;
input rst_i;
input mealy_i;
output logic mealy_o;

typedef enum logic [1:0]{ // Listing all states
	S0 = 2'b00,
	S1 = 2'b01,
	S2 = 2'b10,
	S3 = 2'b11
} state_t;

state_t state, next_state;

always_comb begin : next_state_logic
	
	mealy_o = 1'b0;
	
	case(state)
		S0: begin
			if (mealy_i)
				next_state = S1;
			else
				next_state = S0;
		end
		S1: begin
			if(mealy_i)
				next_state = S1;
			else
				next_state = S2;
		end
		S2: begin
			if(mealy_i)
				next_state = S3;
			else
				next_state = S0;
		end
		S3: begin
			if(mealy_i)
				next_state = S1;
			else begin
				next_state = S0;
				mealy_o = 1'b1;
			end
		end
		default: begin 
			next_state = S0;
		end
	endcase
end

always_ff @(posedge clk_i or negedge rst_i) begin : state_transition

	if (!rst_i)
		state <= S0;
	else
		state <= next_state;

end

endmodule