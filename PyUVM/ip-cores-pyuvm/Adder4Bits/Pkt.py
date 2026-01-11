from pyuvm import *
import random

class Pkt(uvm_sequence_item):


    def __init__(self, name):
        super().__init__(name)
        self.a_i=0
        self.b_i=0
        self.carry_o=0
        self.sum_o=0
    
    def randomize(self):
        self.a_i=random.randint(0, 15)
        self.b_i=random.randint(0, 15)
    