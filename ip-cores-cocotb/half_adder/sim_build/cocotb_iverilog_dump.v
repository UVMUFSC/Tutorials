module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/half_adder.fst");
    $dumpvars(0, half_adder);
end
endmodule
