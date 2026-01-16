"""
MySequencer: UVM sequencer for Mealy FSM.

Coordinates transaction flow between sequence and driver. Acts as the transport
layer for items moving from randomized sequences to the driver.
"""

from pyuvm import uvm_sequencer

class MySequencer(uvm_sequencer):
    """
    UVM sequencer: mediates between sequence and driver.
    
    Operation:
    - Receives items from sequences via sequence.start(sequencer)
    - Delivers items to driver via driver.seq_item_port.get_next_item()
    - Maintains proper handshaking for ordered, synchronized delivery
    """

    def __init__(self, name, parent):
        """
        Initialize sequencer.
        
        Args:
            name: Component name
            parent: Parent component
        """
        super().__init__(name, parent)
    