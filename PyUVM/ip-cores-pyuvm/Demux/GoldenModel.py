"""GoldenModel: Reference model for 1x4 Demux functional verification.

Implements the ideal 1x4 demultiplexer logic: routes single input (x_i) to
one of 4 outputs based on 2-bit selector (sel_i). Other outputs are set to 0.
Used by scoreboard to verify DUT correctness.

Routing logic:
- sel=0 → y0_o=x_i, others=0
- sel=1 → y1_o=x_i, others=0  
- sel=2 → y2_o=x_i, others=0
- sel=3 → y3_o=x_i, others=0
"""

class GoldenModel():
    """Reference demux model: Computes expected outputs for given inputs.
    
    Operation:
    - Decode sel_i to select which output receives x_i input
    - Set other outputs to 0
    - Compare computed expected outputs against observed y0_o-y3_o
    - Return True (pass) or False (fail) for scoreboard logging
    """

    def __init__(self):
        """Initialize model: Set all outputs to 0.
        """
        self.y0=0
        self.y1=0
        self.y2=0
        self.y3=0

    def check(self, packet):
        """Verify DUT output correctness for a transaction.
        
        Args:
            packet: Pkt object with x_i, sel_i, y0_o, y1_o, y2_o, y3_o
            
        Returns:
            True if outputs match expected routing, False otherwise
            
        Operation:
        1. Use sel_i to route x_i to correct output
        2. Set all other outputs to 0
        3. Compare expected vs actual outputs
        4. Return pass/fail for scoreboard
        """
        match packet.sel_i:

            case 0:
                self.y0 = packet.x_i
                self.y1 = 0
                self.y2 = 0
                self.y3 = 0
            case 1:
                self.y1 = packet.x_i
                self.y0 = 0
                self.y2 = 0
                self.y3 = 0
            case 2:
                self.y2 = packet.x_i
                self.y1 = 0
                self.y0 = 0
                self.y3 = 0
            case 3:
                self.y3 = packet.x_i
                self.y1 = 0
                self.y2 = 0
                self.y0 = 0
            

        if (packet.y0_o, packet.y1_o, packet.y2_o, packet.y3_o) == (self.y0, self.y1, self.y2, self.y3):
            return True
        else:
            return False