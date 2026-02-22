//------------------------------------------------------------------------------
// RTL: Half Adder.
// Computes sum (s) and carry (c) from single-bit inputs a and b.
//------------------------------------------------------------------------------
module half_adder(
	a,
	b,
	c,
	s
);

	// Single-bit inputs.
	input a,b;
	// Single-bit outputs.
	output c,s;
	
	// Combinational half-adder equations.
	xor(s, a, b);
	and(c, a, b);
	
endmodule