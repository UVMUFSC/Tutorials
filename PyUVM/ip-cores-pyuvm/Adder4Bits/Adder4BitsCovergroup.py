

"""
Adder4BitsCovergroup: Functional coverage specification for 4-bit Adder.

Defines coverage bins for input combinations to measure functional completeness.
Includes coverpoints for individual inputs and cross-coverage for combinations.
UVM uses this to track when 100% of interesting scenarios have been exercised.
"""

from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross, bin_array, report_coverage

@covergroup
class Adder4BitsCovergroup():
    """
    Coverage group: defines bins for 4-bit adder inputs.
    
    Coverpoints:
    - cp1: Input A bins (zero, low, mid, max, boundary)
    - cp2: Input B bins (zero, low, mid, max, boundary)
    - cp1X2: Cross-coverage for A×B combinations
    
    Target: 100% coverage of all bin combinations.
    """

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
        """Generate coverage report at end of simulation."""
        report_coverage(details=False)
