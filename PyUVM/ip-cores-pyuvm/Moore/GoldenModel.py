"""Moore FSM Golden Reference Model.

Provides reference behavior for Moore state machine verification.
Implements the expected state transitions and outputs.

Moore Machine Specification:
- 5 States: S0 (0), S1 (1), S2 (2), S3 (3), S4 (4)
- State Transitions: Based on next_i input
- Output: Depends only on current state (Moore characteristic)
  - S0-S3: out_o = 0
  - S4: out_o = 1
- Reset: Asynchronous active-high reset to S0

State Transition Table:
- S0: next_i=1 -> S1, next_i=0 -> stay
- S1: next_i=0 -> S2, next_i=1 -> stay
- S2: next_i=1 -> S3, next_i=0 -> S0
- S3: next_i=1 -> S4, next_i=0 -> S2
- S4: next_i=0 -> S2, next_i=1 -> S1
"""

class GoldenModel():
    """Golden reference model for Moore FSM.
    
    Attributes:
        - out: Expected output value
        - previous_state: State before transition
        - current_state: Expected state after transition
    
    The model predicts state transitions and outputs based on Moore FSM rules.
    """
    def __init__(self):
        """Initialize golden model with reset state."""
        self.out=0
        self.previous_state=0
        self.current_state=0

    def check(self, packet):
        """Check DUT transaction against golden model.
        
        Args:
            packet: Transaction packet from monitor
        
        Returns:
            True if DUT matches expected behavior, False otherwise
        
        Process:
            1. Determine output based on previous state (Moore)
            2. Calculate next state based on previous state and next_i
            3. Apply reset if rst_i is active
            4. Compare with DUT's output and state
        """
        self.previous_state = packet.previous_state

        match packet.previous_state:
            case 0:
                self.out = 0
                if(packet.next_i):
                    self.current_state = 1
            case 1:
                self.out = 0
                if(not packet.next_i):
                    self.current_state = 2
                else:
                    self.current_state = 1
            case 2:
                self.out = 0
                if(packet.next_i):
                    self.current_state = 3
                else:
                    self.current_state = 0
            case 3:
                self.out = 0
                if(packet.next_i):
                    self.current_state = 4
                else:
                    self.current_state = 2
            case 4:
                self.out = 1
                if(packet.next_i):
                    self.current_state = 1
                else:
                    self.current_state = 2
            case _:
                self.out = 0
                self.current_state = 0

        match packet.rst_i:
            case 1:
                self.out = 0
                self.current_state = 0

        if (self.out, self.previous_state, self.current_state) == (packet.out_o, packet.previous_state, packet.current_state):
            return True
        else:
            return False