"""
Pkt: Transaction object for 4x1 Mux verification.

Represents a single test vector with input and output fields.
Used to transport transactions through the UVM chain: sequence -> sequencer ->
driver -> BFM -> DUT, and back through monitor for scoreboard checking.
"""

from pyuvm import *
import random

class Pkt(uvm_sequence_item):
    """
    Transaction packet for 4x1 Mux.
    
    Fields:
    - x0_i, x1_i, x2_i, x3_i: input data lines (0-1 each)
    - sel_i: selector signal (0-3)
    - y_o: output result (set by monitor after DUT execution)
    """

    def __init__(self, name):
        super().__init__(name)
        self.x0_i = 0
        self.x1_i = 0
        self.x2_i = 0
        self.x3_i = 0
        self.sel_i = 0
        self.y_o = 0

    def __str__(self):
        return (f"X0={self.x0_i}, X1={self.x1_i}, X2={self.x2_i}, X3={self.x3_i}, SEL={self.sel_i} -> Y={self.y_o}")
    
    def randomize(self):
        """
        Randomize input fields for stimulus generation.
        
        Called by sequence to generate random test vectors.
        Outputs are populated later by the monitor.
        """
        self.x0_i = random.randint(0, 1)
        self.x1_i = random.randint(0, 1)
        self.x2_i = random.randint(0, 1)
        self.x3_i = random.randint(0, 1)
        self.sel_i = random.randint(0, 3)
    