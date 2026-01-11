from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross



@covergroup
class DemuxCovergroup():

    def __init__(self):
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

