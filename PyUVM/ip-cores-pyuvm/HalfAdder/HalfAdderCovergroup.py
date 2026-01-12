from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross

@covergroup
class HalfAdderCovergroup():

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

