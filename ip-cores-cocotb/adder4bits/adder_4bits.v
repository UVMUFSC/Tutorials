module adder_4bits (a_i, b_i, s_o, c_o);
input  [3:0] a_i, b_i;
output [3:0] s_o;
output       c_o;
wire [2:0] w_carry;
half_adder U0(
    .a(a_i[0]),
    .b(b_i[0]),
    .s(s_o[0]),
    .c(w_carry[0])
);
full_adder U1 (
    .a_i(a_i[1]),
    .b_i(b_i[1]),
    .carry_i(w_carry[0]),
    .sum_o(s_o[1]),
    .carry_o(w_carry[1])
);
full_adder U2 (
    .a_i(a_i[2]),
    .b_i(b_i[2]),
    .carry_i(w_carry[1]),
    .sum_o(s_o[2]),
    .carry_o(w_carry[2])
);
full_adder U3 (
    .a_i(a_i[3]),
    .b_i(b_i[3]),
    .carry_i(w_carry[2]),
    .sum_o(s_o[3]),
    .carry_o(c_o)
);
endmodule