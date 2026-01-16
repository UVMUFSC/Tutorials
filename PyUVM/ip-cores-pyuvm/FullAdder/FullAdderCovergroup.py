"""
FullAdderCovergroup: Functional coverage specification for Full Adder.

Defines coverage bins for input combinations (a_i, b_i, carry_i) to measure functional completeness.
Includes coverpoints for individual inputs and cross-coverage for all combinations.
UVM uses this to track when 100% of interesting scenarios have been exercised.
"""

from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross

@covergroup
class HalfAdderCovergroup():
    """
    Coverage group: defines bins for Full Adder inputs (a_i, b_i, carry_i).
    
    Coverpoints:
    - cp1: Input a_i bins (0, 1)
    - cp2: Input b_i bins (0, 1)
    - cp3: Input carry_i bins (0, 1)
    - cp1X2: Cross-coverage for a_i × b_i × carry_i combinations (8 total bins)
    
    Target: 100% coverage of all 8 input combinations.
    """

    def __init__(self):
        self.with_sample(
            a=bit_t(1),
            b=bit_t(1),
            c=bit_t(1)
        )
        self.cp1 = coverpoint(self.a, bins={
            "a_0" : bin(0), "a_1" : bin(1)
            })
        self.cp2 = coverpoint(self.b, bins={
            "b_o" : bin(0), "b_1" : bin(1)
            })
        self.cp3 = coverpoint(self.c, bins={
            "c_o" : bin(0), "c_1" : bin(1)
            })


        self.cp1X2 = cross([self.cp1, self.cp2, self.cp3])

