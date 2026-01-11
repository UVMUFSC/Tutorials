# Makefile - VERSÃO FINAL E CORRETA

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

# Usamos apenas o RTL original
VERILOG_SOURCES += half_adder.v

# Seu módulo de teste completo
COCOTB_TEST_MODULES = test_half_adder

# O TOPLEVEL é o half_adder
TOPLEVEL = half_adder

include $(shell cocotb-config --makefiles)/Makefile.sim