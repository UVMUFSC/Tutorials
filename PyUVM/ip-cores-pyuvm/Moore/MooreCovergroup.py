"""Moore FSM Functional Coverage Definitions.

Defines coverage bins for Moore state machine verification.
Tracks all input values and valid state transitions.

Coverage Goals:
- All next_i input values (0, 1)
- All valid state transitions encoded as 6-bit values:
  - Bits [5:3]: previous_state (0-4)
  - Bits [2:0]: current_state (0-4)

Valid State Transitions (encoded):
- 0: S0->S0, 1: S0->S1, 9: S1->S1, 10: S1->S2
- 16: S2->S0, 19: S2->S3, 26: S3->S2, 28: S3->S4
- 33: S4->S1, 34: S4->S2
"""

from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross, bin_array



@covergroup
class MooreCovergroup():
    """Coverage group for Moore FSM verification.
    
    Coverpoints:
        - cp1: next_i input (bins: next_0, next_1)
        - cp2: state transitions (bins: valid_states array)
    
    Ensures complete exploration of Moore FSM behavior.
    """

    def __init__(self):
        """Initialize covergroup with sampling variables.
        
        Sample parameters:
            - next: 1-bit next_i input
            - state: 6-bit encoded state transition
        """
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


        

