typedef enum logic [3:0] { // Lisiting all opcodes 
  INC = 4'b0000,  		// Increment A
	DEC = 4'b0001, 			// Decrement A
	ADD = 4'b0010,			// Add A to B
	ADD_C = 4'b0011,		// Add B to A with carry
	SUB_B = 4'b0100,		// Subtraction with borrow
	SUB = 4'b0101,			// Subtraction
	SHIFT_R = 4'b0110,	    // Right shift
	SHIFT_L = 4'b0111,	    // Left shift
	AND_OP = 4'b1000,		// A AND B
	NAND = 4'b1001,			// A NAND B
	OR = 4'b1010,			// A OR B
	NOR = 4'b1011,			// A NOR B
	XOR = 4'b1100,			// A XOR B
	XNOR = 4'b1101,			// A NOT B
	NOT = 4'b1110,			// Transfer A
	TRF_A = 4'b1111
} opcode_t;

module alu #(parameter N = 8)( // 8 bit parameter as default
	A_i, 
	B_i,
	opcode_i,
	alu_o,
	carry_o
);

	input logic [N-1:0] A_i, B_i;   // Two basic operands
	input opcode_t opcode_i;        // Selection of opcode
	output logic [N-1:0] alu_o;     // Result of the operation
	output logic carry_o;           // Carry of the operation

	logic [N:0] tmp;
	assign tmp = {1'b0,A_i} + {1'b0,B_i};   // tmp will store the carry bit of the sum, by
	assign carry_o = tmp[N];                // extending the two operands and adding them

	always_comb begin
		case (opcode_i)	// Switch case for the opcode
			INC: alu_o = A_i + 1;
			DEC: alu_o = A_i - 1;
			ADD: alu_o = A_i + B_i;
			ADD_C: alu_o = A_i + B_i + 1;
			SUB_B: alu_o = A_i - B_i;
			SUB: alu_o = A_i - B_i - 1;
			SHIFT_R: alu_o = A_i >> B_i;
			SHIFT_L: alu_o = A_i << B_i;
			AND_OP: alu_o = A_i & B_i;
			NAND: alu_o = ~(A_i & B_i);
			OR: alu_o = A_i | B_i;
			NOR: alu_o = ~(A_i | B_i);
			XOR: alu_o = A_i ^ B_i;
			XNOR: alu_o = ~(A_i ^ B_i);
			TRF_A: alu_o = A_i;
			default: alu_o = 0;
		endcase
	end
endmodule