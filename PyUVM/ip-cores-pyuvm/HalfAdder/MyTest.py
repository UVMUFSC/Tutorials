import pyuvm
from pyuvm import *
from MyPackage import *
from cocotb.triggers import Timer

@pyuvm.test()

class MyTest(uvm_test):    
    def build_phase(self):
        self.env=MyEnv.create("env", self)
        self.bfm = HalfAdderWrapper()
        ConfigDB().set(self, "*", "BUS_BFM", self.bfm)
        self.bfm.start_bfm()

    async def run_phase(self):

        self.raise_objection()

        await Timer(2, unit="ns")

        seqr=self.env.agent.sequencer
        seq=MySequence.create("seq")
        await seq.start(seqr)

        self.drop_objection()