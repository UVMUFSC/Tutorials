from pyuvm import *
from MyAgent import MyAgent
from MyScoreboard import MyScoreboard
from MyCoverage import MyCoverage



"""
MyEnv: UVM environment for 4-bit Adder verification.

Instantiates and connects all verification components (agent, scoreboard,
coverage) into a cohesive testbench architecture. Serves as the container
for the entire verification infrastructure.
"""

class MyEnv(uvm_env):
    """
    UVM environment: instantiates and connects testbench components.
    
    Operation:
    - Creates agent (sequencer, driver, monitor coordination)
    - Creates scoreboard (reference model verification)
    - Creates coverage collector (functional coverage metrics)
    - Registers handles in ConfigDB for global access
    - Connects monitor outputs to scoreboard and coverage inputs
    """

    def __init__(self, name, parent):
        super().__init__(name, parent)
    
    def build_phase(self):
        """
        Build Phase: Instantiate all testbench components.
        
        Creates agent, scoreboard, coverage and registers key handles
        in ConfigDB for access by sequences and other components.
        """
        self.agent = MyAgent.create("agent", self)
        self.scoreboard = MyScoreboard.create("scoreboard", self)
        self.coverage = MyCoverage.create("coverage", self)
        ConfigDB().set(uvm_root(), "", "SEQR", self.agent.sequencer)
        ConfigDB().set(uvm_root(), "", "COV_HANDLE", self.coverage)

    def connect_phase(self):
        """
        Connect Phase: Establish dataflow between components.
        
        Connects monitor analysis port to scoreboard and coverage,
        ensuring observed transactions reach verification components.
        """
        self.agent.monitor.ap.connect(self.scoreboard.analysis_export)
        self.agent.monitor.ap.connect(self.coverage.analysis_export)
