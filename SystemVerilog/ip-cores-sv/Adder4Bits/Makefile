# Simple Makefile for UVM + Xcelium
XRUN = xrun -64bit -uvm -sv
RUN_F = run.f
TEST = my_test
VERBOSITY = UVM_LOW

# Main target: compile and run
run: clean
	$(XRUN) -f $(RUN_F) -coverage all -covoverwrite +UVM_TESTNAME=$(TEST) +UVM_VERBOSITY=$(VERBOSITY) 

# Compile, run and save it in a log
run_log: clean
	$(XRUN) -f $(RUN_F) -coverage all -covoverwrite +UVM_TESTNAME=$(TEST) +UVM_VERBOSITY=$(VERBOSITY) | tee simulation.log

# Clean generated simulation artifacts
clean:
	rm -rf xcelium.d xrun.history xrun.log waves.shm cov_work

# Open with SimVision
gui: 
	$(XRUN) -f $(RUN_F) -coverage all -covoverwrite +UVM_TESTNAME=$(TEST) -gui