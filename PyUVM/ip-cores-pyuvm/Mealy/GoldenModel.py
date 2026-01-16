"""
Mealy Machine Verification - Golden Model

Reference implementation of Mealy FSM for correctness checking.

Key Mealy Characteristic:
- Output (mealy_o) depends on BOTH current state AND input
- Contrast with Moore: output depends only on current state

State Diagram:
- State 0: input=1 -> State 1; input=0 -> State 0
- State 1: input=1 -> State 1; input=0 -> State 2
- State 2: input=1 -> State 3; input=0 -> State 0
- State 3: input=1 -> State 1; input=0 -> State 0 (mealy_o=1)
- Reset (rst_i=0): State 0, mealy_o=0
"""

class GoldenModel():
    """
    Mealy FSM Golden Reference Model
    
    Implements expected behavior for comparison with DUT.
    
    Attributes:
        mealy_o: Expected output (depends on state + input)
        next_state: Expected next state
        current_state: Current state
    
    Key Difference from Moore:
    - Output is combinational (depends on current_state + mealy_i)
    - Moore output would depend only on current_state
    """
    def __init__(self):
        """
        Initialize golden model state variables.
        """
        self.mealy_o=0
        self.next_state=0
        self.current_state=0

    def check(self, packet):
        """
        Verify packet against expected Mealy FSM behavior.
        
        Args:
            packet: Pkt with current_state, mealy_i, rst_i, mealy_o, next_state
        
        Returns:
            True if DUT matches golden model, False otherwise
        
        Logic:
        - Reset (rst_i=0): next_state=0, mealy_o=0
        - Normal operation: compute next_state and mealy_o based on
          current_state and mealy_i (Mealy characteristic)
        """
        self.current_state = packet.current_state
        self.mealy_o = 0

        if(packet.rst_i == 0):
            self.next_state = 0
            self.mealy_o = 0
                
        else:
            match packet.current_state:
                case 0:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 0
                case 1:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 2
                case 2:
                    if(packet.mealy_i):
                        self.next_state = 3
                    else:
                        self.next_state = 0
                case 3:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 0
                        self.mealy_o = 1
                case _:
                    self.mealy_o = 0
                    self.next_state = 0


        if (self.mealy_o, self.current_state, self.next_state) == (packet.mealy_o, packet.current_state, packet.next_state):
            return True
        else:
            return False