module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/mux4x1.fst");
    $dumpvars(0, mux4x1);
end
endmodule
