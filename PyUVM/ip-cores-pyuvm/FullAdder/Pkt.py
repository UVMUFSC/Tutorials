"""Pkt: Transaction packet for Full Adder verification.

Encapsulates full adder inputs and outputs for a single transaction:
- Inputs: a_i, b_i, carry_i (1-bit each, form the 3-input adder)
- Outputs: sum_o (XOR of all 3 inputs), carry_o (majority logic of inputs)

Full adder logic:
- sum_o = a_i ⊕ b_i ⊕ carry_i
- carry_o = (a_i & b_i) | (a_i & carry_i) | (b_i & carry_i)
"""

from pyuvm import *
import random

class Pkt(uvm_sequence_item):
    """Transaction packet: Represents full adder inputs/outputs.
    
    Fields:
    - a_i: First input bit
    - b_i: Second input bit
    - carry_i: Carry input bit
    - sum_o: Sum output (XOR of a, b, carry_i)
    - carry_o: Carry output (majority logic)
    
    Randomization: Randomizes all 3 inputs; outputs are DUT-generated.
    """


    def __init__(self, name):
        super().__init__(name)
        self.a_i=0
        self.b_i=0
        self.carry_i=0
        self.carry_o=0
        self.sum_o=0
    
    def randomize(self):
        """Randomize input fields for stimulus generation.
        
        a_i, b_i, carry_i: random 1-bit values (0 or 1)
        Outputs (sum_o, carry_o) are not randomized (DUT drives them).
        """
        self.a_i=random.randint(0, 1)
        self.b_i=random.randint(0, 1)
        self.carry_i=random.randint(0, 1)
    