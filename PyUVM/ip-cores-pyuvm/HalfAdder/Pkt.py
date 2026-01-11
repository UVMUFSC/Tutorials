from pyuvm import *
import random

class Pkt(uvm_sequence_item):


    def __init__(self, name):
        super().__init__(name)
        self.c=0
        self.s=0
        self.a=0
        self.b=0

    def __str__(self):
        return (f"A={self.a}, B={self.b} -> S={self.s}, C={self.c}")
    
    def randomize(self):
        self.a=random.randint(0, 1)
        self.b=random.randint(0, 1)
    