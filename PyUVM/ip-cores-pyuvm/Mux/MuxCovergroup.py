"""
MuxCovergroup: Functional coverage model for 4x1 Mux DUT.

Defines coverage bins for all input combinations (4 data lines + 2-bit selector).
Includes cross-coverage between data inputs and selector value to ensure all
routing paths are exercised during verification.

Coverage bins:
- Individual coverpoints for x0_i, x1_i, x2_i, x3_i (each: 0 or 1)
- Coverpoint for sel_i selector (00, 01, 10, 11)
- Cross coverage: All combinations of inputs × selector values
"""

from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross



@covergroup
class MuxCovergroup():
    """
    Functional coverage: Measures exercised input/selector combinations.
    
    Tracks:
    - Individual values of each data input (x0_i through x3_i)
    - All selector states (sel_i: 0, 1, 2, 3 representing binary 00, 01, 10, 11)
    - Cross coverage between selector and all data lines (ensures each input
      is selected by each selector state)
    """

    def __init__(self):
        """
        Initialize coverage model with individual coverpoints and cross coverage.
        
        Coverpoints:
        - cp1-cp4: Individual input lines (x0_i, x1_i, x2_i, x3_i) = 2 bins each (0/1)
        - cp5: Selector line (sel_i) = 4 bins (0/1/2/3)
        - cp1X2: Cross of all 5 coverpoints (ensures each input is selected)
        """
        self.with_sample(
            x0=bit_t(1),
            x1=bit_t(1),
            x2=bit_t(1),
            x3=bit_t(1),
            sel=bit_t(2)
        )
        self.cp1 = coverpoint(self.x0, bins={
            "x0_0" : bin(0), "x0_1" : bin(1)
            })
        self.cp2 = coverpoint(self.x1, bins={
            "x1_0" : bin(0), "x1_1" : bin(1)
            })
        self.cp3 = coverpoint(self.x2, bins={
            "x2_0" : bin(0), "x2_1" : bin(1)
            })
        self.cp4 = coverpoint(self.x3, bins={
            "x3_0" : bin(0), "x3_1" : bin(1)
            })
        self.cp5 = coverpoint(self.sel, bins={
            "sel_00" : bin(0), "sel_01" : bin(1), "sel_10" : bin(2), "sel_11" : bin(3)
            })

        self.cp1X2 = cross([self.cp1, self.cp2, self.cp3, self.cp4, self.cp5])

