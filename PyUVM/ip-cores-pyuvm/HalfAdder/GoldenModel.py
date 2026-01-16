"""
GoldenModel: Reference model for Half Adder functional verification.

Computes expected outputs for comparison with DUT:
- sum = a XOR b
- carry = a AND b
"""

class GoldenModel():
    """
    Golden reference for Half Adder logic.
    
    Implements expected behavior:
    - sum_o = a_i XOR b_i
    - carry_o = a_i AND b_i
    """

    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):
        """
        Verify packet against expected Half Adder behavior.
        
        Returns:
        - True if DUT outputs match expected values
        - False otherwise
        """
        self.s=packet.a ^ packet.b
        self.c = packet.a & packet.b

        if packet.s == self.s and packet.c == self.c:
            return True
        else:
            return False