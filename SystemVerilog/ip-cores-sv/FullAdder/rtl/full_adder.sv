module full_adder(
    a_i,
    b_i,
    carry_i,
    sum_o,
    carry_o
    );

    input a_i, b_i, carry_i;
    output sum_o, carry_o;
    wire w_sum, w_carry1, w_carry2;

    half_adder U1(
    .a(a_i),
    .b(b_i),
    .s(w_sum),
    .c(w_carry1)
    );

    half_adder U2(
    .a(w_sum),
    .b(carry_i),
    .s(sum_o),
    .c(w_carry2)
    );

    or U3(carry_o, w_carry1, w_carry2);

endmodule