module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/adder_4bits.fst");
    $dumpvars(0, adder_4bits);
end
endmodule
