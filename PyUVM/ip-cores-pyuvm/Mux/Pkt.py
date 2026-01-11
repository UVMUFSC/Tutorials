from pyuvm import *
import random

class Pkt(uvm_sequence_item):


    def __init__(self, name):
        super().__init__(name)
        self.x0_i=0
        self.x1_i=0
        self.x2_i=0
        self.x3_i=0
        self.sel_i=0
        self.y_o=0

    def __str__(self):
        return (f"X0={self.x0_i}, X1={self.x1_i}, X2={self.x2_i}, X3={self.x3_i}, SEL={self.sel_i} -> Y={self.y_o}")
    
    def randomize(self):
        self.x0_i=random.randint(0, 1)
        self.x1_i=random.randint(0, 1)
        self.x2_i=random.randint(0, 1)
        self.x3_i=random.randint(0, 1)
        self.sel_i=random.randint(0, 3)
    