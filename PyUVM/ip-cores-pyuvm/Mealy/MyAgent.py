from pyuvm import *
from MyDriver import MyDriver
from MySequencer import MySequencer
from MyMonitor import MyMonitor

class MyAgent(uvm_agent):
    def __init__(self, name, parent, is_active=True):
        super().__init__(name, parent)
        self.sequencer=None
        self.is_active=is_active

    def build_phase(self):
        self.sequencer=MySequencer.create("sequencer", self)
        if self.is_active:
            self.driver=MyDriver.create("driver", self)
        self.monitor=MyMonitor.create("monitor", self)

    def connect_phase(self):
        if self.is_active:
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export)