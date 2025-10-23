module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/full_adder.fst");
    $dumpvars(0, full_adder);
end
endmodule
