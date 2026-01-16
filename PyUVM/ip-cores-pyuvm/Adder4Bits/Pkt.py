

"""
Pkt: Transaction object for 4-bit Adder verification.

Represents a single test vector with input and output fields.
Used to transport transactions through the UVM chain: sequence -> sequencer ->
driver -> BFM -> DUT, and back through monitor for scoreboard checking.
"""

from pyuvm import *
import random

class Pkt(uvm_sequence_item):
    """
    Transaction packet for 4-bit Adder.
    
    Fields:
    - a_i, b_i: input operands (0-15)
    - carry_o, sum_o: output results (set by monitor after DUT execution)
    """

    def __init__(self, name):
        super().__init__(name)
        self.a_i = 0
        self.b_i = 0
        self.carry_o = 0
        self.sum_o = 0
    
    def randomize(self):
        """
        Randomize input fields for stimulus generation.
        
        Called by sequence to generate random test vectors.
        Outputs are populated later by the monitor.
        """
        self.a_i = random.randint(0, 15)
        self.b_i = random.randint(0, 15)
    