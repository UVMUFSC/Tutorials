"""GoldenModel: Reference model for Full Adder functional verification.

Implements the ideal full adder logic: computes sum and carry outputs for 3-bit
input. Used by scoreboard to verify DUT correctness.

Full adder equations:
- sum = a ⊕ b ⊕ carry_i (3-input XOR)
- carry_o = (a & b) | (a & carry_i) | (b & carry_i) (majority logic)
"""

class GoldenModel():
    """Reference full adder model: Computes expected outputs for given inputs.
    
    Operation:
    - Compute sum using 3-input XOR
    - Compute carry using majority logic (carry when 2+ inputs are 1)
    - Compare computed outputs against observed DUT outputs
    - Return True (pass) or False (fail) for scoreboard logging
    """

    def __init__(self):
        """Initialize model: Set sum and carry to 0.
        """
        self.s=0
        self.c=0

    def check(self, packet):
        """Verify DUT output correctness for a transaction.
        
        Args:
            packet: Pkt object with a_i, b_i, carry_i, sum_o, carry_o
            
        Returns:
            True if both sum_o and carry_o match expected values, False otherwise
            
        Operation:
        1. Compute expected sum (3-input XOR)
        2. Compute expected carry (majority logic)
        3. Compare expected vs actual outputs
        4. Return pass/fail for scoreboard
        """
        self.s=packet.a_i ^ packet.b_i ^ packet.carry_i
        self.c = (packet.a_i & packet.b_i) | (packet.a_i & packet.carry_i) | (packet.b_i & packet.carry_i)

        if packet.sum_o == self.s and packet.carry_o == self.c:
            return True
        else:
            return False