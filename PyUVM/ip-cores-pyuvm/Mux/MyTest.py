"""
MyTest: Top-level UVM test for 4x1 Mux verification.

Orchestrates the verification flow: instantiates testbench components, launches
coverage-driven stimulus generation, and runs until functional coverage goal.
"""

import pyuvm
from pyuvm import *
from MyPackage import *
from cocotb.triggers import Timer

@pyuvm.test()
class MyTest(uvm_test):
    """
    Top-level test: coordinates all UVM components and test execution.
    
    Responsibilities:
    - Builds testbench hierarchy (environment, BFM)
    - Registers BFM in ConfigDB for driver/monitor access
    - Starts BFM background tasks (driver_task, monitor_task)
    - Launches stimulus sequence and manages simulation objections
    """

    def build_phase(self):
        """
        Build Phase: Construct testbench hierarchy and register BFM.
        
        Creates environment (agent, scoreboard, coverage), instantiates
        BFM wrapper, registers it globally, and starts background tasks.
        """
        self.env = MyEnv.create("env", self)
        self.bfm = MuxWrapper()
        ConfigDB().set(self, "*", "BUS_BFM", self.bfm)
        self.bfm.start_bfm()

    async def run_phase(self):
        """
        Run Phase: Execute stimulus until coverage goal is reached.
        
        Flow:
        1. Raise objection (prevent premature end)
        2. Wait for DUT initialization
        3. Start coverage-driven sequence
        4. Drop objection when complete (coverage = 100%)
        """
        self.raise_objection()
        await Timer(2, unit="ns")
        seqr = self.env.agent.sequencer
        seq = MySequence.create("seq")
        await seq.start(seqr)
        self.drop_objection()