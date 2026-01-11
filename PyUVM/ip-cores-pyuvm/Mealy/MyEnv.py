from pyuvm import *
from MyAgent import MyAgent
from MyScoreboard import MyScoreboard
from MyCoverage import MyCoverage

class MyEnv(uvm_env):
    def __init__(self, name, parent):
        super().__init__(name, parent)
    
    def build_phase(self):
        self.agent=MyAgent.create("agent", self)
        self.scoreboard=MyScoreboard.create("scoreboard", self)
        self.coverage=MyCoverage.create("coverage", self)
        ConfigDB().set(uvm_root(), "", "SEQR", self.agent.sequencer)
        ConfigDB().set(uvm_root(), "", "COV_HANDLE", self.coverage)

    def connect_phase(self):
        self.agent.monitor.ap.connect(self.scoreboard.analysis_export)
        self.agent.monitor.ap.connect(self.coverage.analysis_export)
