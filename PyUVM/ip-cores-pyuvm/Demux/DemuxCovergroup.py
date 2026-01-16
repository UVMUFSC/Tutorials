"""DemuxCovergroup: Functional coverage model for 1x4 Demux DUT.

Defines coverage bins for input and selector combinations. Ensures all routing
paths are exercised (each selector state with both input values).

Coverage bins:
- Coverpoint for x_i input (0 or 1)
- Coverpoint for sel_i selector (00, 01, 10, 11)
- Cross coverage: input × selector (verifies each routing path is tested)
"""

from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross



@covergroup
class DemuxCovergroup():
    """Functional coverage: Measures exercised input/selector combinations.
    
    Tracks:
    - Input values (x_i: 0 or 1)
    - Selector states (sel_i: 0, 1, 2, 3 for routing to y0_o, y1_o, y2_o, y3_o)
    - Cross coverage between input and selector (ensures each path is tested)
    """

    def __init__(self):
        """Initialize coverage model with coverpoints and cross coverage.
        
        Coverpoints:
        - cp1: Input line (x_i) = 2 bins (0/1)
        - cp2: Selector line (sel_i) = 4 bins (0/1/2/3)
        - cp1X2: Cross of input × selector (ensures all routing paths exercised)
        """
        self.with_sample(
            x=bit_t(1),
            sel=bit_t(2)
        )
        self.cp1 = coverpoint(self.x, bins={
            "x_0" : bin(0), "x_1" : bin(1)
            })
        self.cp2 = coverpoint(self.sel, bins={
            "sel_00" : bin(0), "sel_01" : bin(1), "sel_10" : bin(2), "sel_11" : bin(3)
            })

        self.cp1X2 = cross([self.cp1, self.cp2])

