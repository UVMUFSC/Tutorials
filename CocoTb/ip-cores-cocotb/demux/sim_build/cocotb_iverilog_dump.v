module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/demux1x4.fst");
    $dumpvars(0, demux1x4);
end
endmodule
