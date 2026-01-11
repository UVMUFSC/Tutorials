from pyuvm import *
import random

class Pkt(uvm_sequence_item):


    def __init__(self, name):
        super().__init__(name)
        self.next_i=0
        self.rst_i=0
        self.out_o=0
        self.previous_state=0
        self.current_state=0

    def __str__(self):
        return (f"PREVIOUS_STATE={self.previous_state}, CURRENT_STATE={self.current_state}, NEXT={self.next_i}, RST={self.rst_i} -> OUT={self.out_o}")
    
    def randomize(self):
        self.next_i=random.randint(0, 1)
        self.rst_i=random.randint(0, 1)
    