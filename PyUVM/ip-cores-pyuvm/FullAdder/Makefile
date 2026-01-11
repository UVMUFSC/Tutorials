SIM ?= verilator
TOPLEVEL_LANG ?= verilog
WAVES=1
VERILOG_SOURCES += $(PWD)/full_adder.sv
COCOTB_TOPLEVEL = full_adder
COCOTB_TEST_MODULES = MyTest
include $(shell cocotb-config --makefiles)/Makefile.sim