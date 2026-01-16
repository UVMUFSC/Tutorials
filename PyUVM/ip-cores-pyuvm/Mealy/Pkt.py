"""
Mealy Machine Verification - Transaction Packet

Defines the transaction item for Mealy FSM verification.
In Mealy machines, output depends on both current state and inputs.

Signals:
    - mealy_i: Input signal (0 or 1)
    - rst_i: Reset signal (active low)
    - mealy_o: Output signal (depends on current state + input)
    - current_state: Current FSM state (0-3)
    - next_state: Next FSM state (0-3)
"""

from pyuvm import *
import random

class Pkt(uvm_sequence_item):
    """
    Mealy FSM Transaction Packet
    
    Encapsulates all signals for Mealy machine verification:
    - Input: mealy_i (data input)
    - Reset: rst_i (active low reset)
    - Output: mealy_o (combinational output based on state + input)
    - State tracking: current_state, next_state
    """

    def __init__(self, name):
        """
        Initialize transaction packet.
        
        Args:
            name: Unique identifier for this packet
        """
        super().__init__(name)
        self.mealy_i=0
        self.rst_i=0
        self.mealy_o=0
        self.next_state=0
        self.current_state=0

    def __str__(self):
        """
        String representation showing state transition and I/O.
        
        Returns:
            Formatted string: CURRENT_STATE -> NEXT_STATE with inputs/outputs
        """
        return (f"CURRENT_STATE={self.current_state}, NEXT_STATE={self.next_state} INPUT={self.mealy_i}, RST={self.rst_i} -> OUTPUT={self.mealy_o}")
    
    def randomize(self):
        """
        Generate random inputs for stimulus.
        
        Randomizes:
            - mealy_i: 0 or 1
            - rst_i: 0 or 1
        """
        self.mealy_i=random.randint(0, 1)
        self.rst_i=random.randint(0, 1)
    