"""Moore FSM UVM Test.

Top-level test class for Moore state machine verification.
Creates the testbench environment and executes the test sequence.

Test Flow:
- Build phase: Create environment and BFM
- Run phase: Execute sequence until 100% coverage achieved
- Check phase: Verify scoreboard and coverage results
"""

import pyuvm
from pyuvm import *
from MyPackage import *
from cocotb.triggers import Timer

@pyuvm.test()

class MyTest(uvm_test):
    """UVM test for Moore FSM verification.
    
    Responsibilities:
        - Create and configure environment
        - Initialize and start BFM
        - Execute test sequence
        - Control test objections for proper phasing
    """    
    def build_phase(self):
        self.env=MyEnv.create("env", self)
        self.bfm = MooreWrapper()
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

        seqr=self.env.agent.sequencer
        seq=MySequence.create("seq")
        await seq.start(seqr)

        self.drop_objection()