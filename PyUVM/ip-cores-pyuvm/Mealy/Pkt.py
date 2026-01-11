from pyuvm import *
import random

class Pkt(uvm_sequence_item):


    def __init__(self, name):
        super().__init__(name)
        self.mealy_i=0
        self.rst_i=0
        self.mealy_o=0
        self.next_state=0
        self.current_state=0

    def __str__(self):
        return (f"CURRENT_STATE={self.current_state}, NEXT_STATE={self.next_state} INPUT={self.mealy_i}, RST={self.rst_i} -> OUTPUT={self.mealy_o}")
    
    def randomize(self):
        self.mealy_i=random.randint(0, 1)
        self.rst_i=random.randint(0, 1)
    