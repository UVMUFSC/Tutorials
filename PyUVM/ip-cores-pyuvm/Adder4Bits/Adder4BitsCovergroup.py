from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross, bin_array, report_coverage



@covergroup
class Adder4BitsCovergroup():

    def __init__(self):
        self.with_sample(
            a=bit_t(4),
            b=bit_t(4),
        )
        self.cp1 = coverpoint(self.a, bins={
            "A_zero": bin(0),         
            "A_low": bin_array([],[1, 6]),           
            "A_mid": bin_array([],[9, 14]),          
            "A_max": bin(15),             
            "A_boundary": bin_array([],[7, 8])
            })
        self.cp2 = coverpoint(self.b, bins={
            "B_zero": bin(0),         
            "B_low": bin_array([],[1, 6]),           
            "B_mid": bin_array([],[9, 14]),          
            "B_max": bin(15),             
            "B_boundary": bin_array([],[7, 8])
            })


        self.cp1X2 = cross([self.cp1, self.cp2])


    def report(self):
        report_coverage(details=False)
