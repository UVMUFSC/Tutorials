#------------------------------------------------------------------------------
# Xcelium file list for compiling the Half Adder testbench.
# Update the paths to match your local environment.
#------------------------------------------------------------------------------
-incdir "path to your uvm files folder"
"path to your package"/half_adder_pkg.sv
"path to your DUT interface"/dut_if.sv
"path to your DUT"/half_adder.sv
"path to your DUT wrapper"/half_adder_wrapper.sv
"path to your testbench top file"/tb_top.sv

# These lines tell Xcelium where to find your files (incdir) and the order in
# which they will be compiled.