SIM ?= verilator
TOPLEVEL_LANG ?= verilog
WAVES=1
VERILOG_SOURCES += $(PWD)/mealy_fsm.sv
COCOTB_TOPLEVEL = mealy_fsm
COCOTB_TEST_MODULES = MyTest
GUI = 1
include $(shell cocotb-config --makefiles)/Makefile.sim