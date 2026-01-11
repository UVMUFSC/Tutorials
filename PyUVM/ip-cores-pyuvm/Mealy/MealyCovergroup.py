from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross, bin_array



@covergroup
class MealyCovergroup():

    def __init__(self):
        self.with_sample(
            state=bit_t(6),
        )
        
        self.cp1 = coverpoint(self.state, bins={
            "valid_states" : bin_array([], 0, 1, 4, 5, 6, 8, 11, 12, 13)
            })
        


        

