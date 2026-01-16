"""
Pkt: Transaction packet for 1x4 Demux verification.

Encapsulates demux inputs and outputs for a single transaction:
- Input: x_i (1-bit data input)
- Selector: sel_i (2-bit selector, routes x_i to one of 4 outputs)
- Outputs: y0_o, y1_o, y2_o, y3_o (4 output lines, only one active per transaction)

Demux routing logic: sel_i selects which output receives x_i value, others = 0
"""

from pyuvm import *
import random

class Pkt(uvm_sequence_item):
    """
    Transaction packet: Represents demux inputs/outputs for a single operation.
    
    Fields:
    - x_i: Data input (1 bit)
    - sel_i: Selector (2 bits = 0-3, selects output line)
    - y0_o, y1_o, y2_o, y3_o: Output lines (1 bit each)
    
    Randomization: Randomizes input and selector; outputs are DUT-generated.
    """


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
        """
        Randomize input fields for stimulus generation.
        
        x_i: random 1-bit value (0 or 1)
        sel_i: random 2-bit selector (0-3)
        Outputs are not randomized (DUT drives them based on inputs).
        """
        self.x_i=random.randint(0, 1)
        self.sel_i=random.randint(0, 3)
    