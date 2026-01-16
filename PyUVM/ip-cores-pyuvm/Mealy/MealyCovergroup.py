"""
Mealy Machine Verification - Coverage Model

Defines functional coverage for Mealy FSM state transitions.

Coverage Strategy:
- Encode state transitions as: (prev_state << 2) | next_state
- Track all valid transitions in Mealy state machine

Valid Transitions:
- 0->0 (bin 0), 0->1 (bin 1)
- 1->0 (bin 4), 1->1 (bin 5), 1->2 (bin 6)
- 2->0 (bin 8), 2->3 (bin 11)
- 3->0 (bin 12), 3->1 (bin 13)
"""

from pyuvm import *
from vsc import covergroup, coverpoint, bit_t, bin, cross, bin_array



@covergroup
class MealyCovergroup():
    """
    Mealy FSM State Transition Covergroup
    
    Tracks coverage of all valid state transitions.
    
    Sampling:
    - state: 6-bit encoded transition (prev_state << 2) | next_state
    
    Bins:
    - valid_states: All legal transitions (0, 1, 4, 5, 6, 8, 11, 12, 13)
    
    Goal: Achieve 100% coverage of all state transitions
    """

    def __init__(self):
        """
        Initialize covergroup with state transition sampling.
        
        Sample point:
        - state: Encoded as (current_state << 2) | next_state
        """
        self.with_sample(
            state=bit_t(6),
        )
        
        self.cp1 = coverpoint(self.state, bins={
            "valid_states" : bin_array([], 0, 1, 4, 5, 6, 8, 11, 12, 13)
            })
        


        

