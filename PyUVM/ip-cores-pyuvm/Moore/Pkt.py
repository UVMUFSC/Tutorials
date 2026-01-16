"""Moore FSM Transaction Packet.

Defines the transaction item for Moore state machine verification.
Contains inputs (next_i, rst_i), outputs (out_o), and state tracking
(previous_state, current_state).

Moore Machine Characteristics:
- Output depends only on current state
- State transitions on clock edge
- Five states: S0-S4
- Single bit output signal
"""

from pyuvm import *
import random

class Pkt(uvm_sequence_item):
    """Transaction packet for Moore FSM verification.
    
    Attributes:
        - next_i: Input signal to control state transitions (1-bit)
        - rst_i: Reset input signal (1-bit, active high)
        - out_o: Output signal from Moore FSM (1-bit)
        - previous_state: State before transition (3-bit)
        - current_state: State after transition (3-bit)
    
    The Moore machine has 5 states (S0-S4) with output depending only on state.
    """

    def __init__(self, name):
        """Initialize Moore FSM transaction packet.
        
        Args:
            name: Identifier for the transaction packet
        """
        super().__init__(name)
        self.next_i=0
        self.rst_i=0
        self.out_o=0
        self.previous_state=0
        self.current_state=0

    def __str__(self):
        """Return formatted string representation of the transaction.
        
        Returns:
            String showing state transition and signals for debugging
        """
        return (f"PREVIOUS_STATE={self.previous_state}, CURRENT_STATE={self.current_state}, NEXT={self.next_i}, RST={self.rst_i} -> OUT={self.out_o}")
    
    def randomize(self):
        """Generate random values for Moore FSM inputs.
        
        Randomizes:
            - next_i: Random bit (0 or 1)
            - rst_i: Random bit (0 or 1)
        """
        self.next_i=random.randint(0, 1)
        self.rst_i=random.randint(0, 1)
    