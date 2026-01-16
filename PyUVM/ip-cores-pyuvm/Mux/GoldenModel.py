"""
GoldenModel: Reference model for 4x1 Mux functional verification.

Implements the ideal 4x1 multiplexer logic: output = input_line selected by
2-bit selector (sel_i). Used by scoreboard to verify DUT correctness for each
transaction by comparing expected vs actual output.

Routing logic: y_o = x0_i (sel=0), x1_i (sel=1), x2_i (sel=2), x3_i (sel=3)
"""

class GoldenModel():
    """
    Reference multiplexer model: Computes expected output for given inputs.
    
    Operation:
    - decode(sel_i) to select which input drives y_o
    - Compare computed expected output against observed y_o
    - Return True (pass) or False (fail) for scoreboard logging
    """

    def __init__(self):
        """
        Initialize model: Set default output to 0.
        """
        self.y=0

    def check(self, packet):
        """
        Verify DUT output correctness for a transaction.
        
        Args:
            packet: Pkt object with x0_i, x1_i, x2_i, x3_i, sel_i, y_o
            
        Returns:
            True if y_o matches selected input, False otherwise
            
        Operation:
        1. Use sel_i selector to route correct input to expected output
        2. Compare expected vs actual y_o
        3. Return pass/fail for scoreboard
        """
        match packet.sel_i:

            case 0:
                self.y = packet.x0_i
            case 1:
                self.y = packet.x1_i
            case 2:
                self.y = packet.x2_i
            case 3:
                self.y = packet.x3_i
            

        if packet.y_o == self.y:
            return True
        else:
            return False