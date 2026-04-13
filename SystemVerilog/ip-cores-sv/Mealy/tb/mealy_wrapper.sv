//------------------------------------------------------------------------------
// DUT wrapper: connects the DUT to the virtual interface and exports
// compact debug signals through data_bus_out.
//------------------------------------------------------------------------------
module mealy_wrapper (dut_if vif);

    // Internal DUT output mirrored from mealy_fsm.
    logic out;

    // Instantiate DUT and map inputs/outputs to the interface.
    mealy_fsm DUT(.clk_i(vif.clk), .rst_i(!(vif.rst)), .mealy_i(vif.data_bus_in), .mealy_o(out));


    // Combinational mapping from DUT internals to monitor-visible bus:
    // [3]=mealy_i, [2:1]=state, [0]=mealy_o.
    assign vif.data_bus_out[3]   = DUT.mealy_i;
    assign vif.data_bus_out[2:1] = DUT.state;
    assign vif.data_bus_out[0]   = DUT.mealy_o;


endmodule
