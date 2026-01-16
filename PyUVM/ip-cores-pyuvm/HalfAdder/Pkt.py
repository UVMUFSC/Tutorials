"""
Pkt: Transaction object for Half Adder verification.

Represents a single test vector with input and output fields.
Used to transport transactions through the UVM chain: sequence -> sequencer ->
driver -> BFM -> DUT, and back through monitor for scoreboard checking.
"""

from pyuvm import *
import random

class Pkt(uvm_sequence_item):
    """
    Transaction packet for Half Adder.
    
    Fields:
    - a_i, b_i: input operands (0-1)
    - sum_o, carry_o: output results (set by monitor after DUT execution)
    """

    def __init__(self, name):
        super().__init__(name)
        self.c=0
        self.s=0
        self.a=0
        self.b=0

    def __str__(self):
        return (f"A={self.a}, B={self.b} -> S={self.s}, C={self.c}")
    
    def randomize(self):
        """
        Randomize input fields for stimulus generation.
        
        Called by sequence to generate random test vectors.
        Outputs are populated later by the monitor.
        """
        self.a=random.randint(0, 1)
        self.b=random.randint(0, 1)
    