

"""
GoldenModel: Reference model for 4-bit Adder.

Implements the expected behavior of the adder. Used by the scoreboard to
compute expected outputs and compare against DUT results. This is the oracle
of correctness for the entire verification.
"""

class GoldenModel():
    """
    Golden model: reference implementation of 4-bit adder behavior.
    
    Computes the expected sum and carry for any input pair, allowing
    the scoreboard to verify DUT outputs are correct.
    """

    def __init__(self):
        self.s = 0
        self.c = 0

    def check(self, packet):
        """
        Check if DUT outputs match expected sum and carry.
        
        Computes expected result from inputs, compares with DUT outputs,
        stores expected values for logging on mismatch.
        
        Returns:
            True if outputs match expected; False otherwise.
        """
        total_sum = int(packet.a_i) + int(packet.b_i)
        self.s = total_sum & 0xF
        self.c = total_sum >> 4
        return (packet.sum_o == self.s and packet.carry_o == self.c)