from pyuvm import uvm_sequencer

class MySequencer(uvm_sequencer):

    def __init__(self, name, parent):
        super().__init__(name, parent)
    