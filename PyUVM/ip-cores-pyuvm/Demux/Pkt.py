from pyuvm import *
import random

class Pkt(uvm_sequence_item):


    def __init__(self, name):
        super().__init__(name)
        self.y0_o=0
        self.y1_o=0
        self.y2_o=0
        self.y3_o=0
        self.sel_i=0
        self.x_i=0

    def __str__(self):
        return (f"X={self.x_i}, SEL={self.sel_i} -> Y0={self.y0_o}, Y1={self.y1_o}, Y2={self.y2_o}, Y3={self.y3_o}")
    
    def randomize(self):
        self.x_i=random.randint(0, 1)
        self.sel_i=random.randint(0, 3)
    