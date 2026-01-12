from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross, bin_array



@covergroup
class MooreCovergroup():

    def __init__(self):
        self.with_sample(
            next=bit_t(1),
            state=bit_t(6),
        )
        
        self.cp1 = coverpoint(self.next, bins={
            "next_0" : bin(0), "next_1" : bin(1)
            })

        self.cp2 = coverpoint(self.state, bins={
            "valid_states" : bin_array([], 0, 1, 9, 10, 16, 19, 26, 28, 33, 34)
            })


        

