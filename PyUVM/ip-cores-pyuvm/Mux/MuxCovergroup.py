from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross



@covergroup
class MuxCovergroup():

    def __init__(self):
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

