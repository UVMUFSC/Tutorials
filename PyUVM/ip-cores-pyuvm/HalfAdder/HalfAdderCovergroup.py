"""
HalfAdderCovergroup: Functional coverage bins for Half Adder inputs.

Defines coverage points for a_i and b_i, plus cross coverage to ensure all
input combinations (2x2 = 4 cases) are tested.
"""

from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross

@covergroup
class HalfAdderCovergroup():
    """
    Coverage model for Half Adder verification.
    
    Coverpoints:
    - a_i: bins for 0 and 1
    - b_i: bins for 0 and 1
    - Cross coverage: all 4 combinations (0,0), (0,1), (1,0), (1,1)
    """

    def __init__(self):
        self.with_sample(
            a=bit_t(1),
            b=bit_t(1)
        )
        self.cp1 = coverpoint(self.a, bins={
            "a_0" : bin(0), "a_1" : bin(1)
            })
        self.cp2 = coverpoint(self.b, bins={
            "b_o" : bin(0), "b_1" : bin(1)
            })

        self.cp1X2 = cross([self.cp1, self.cp2])

