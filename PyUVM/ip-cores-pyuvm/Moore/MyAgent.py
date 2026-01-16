"""
MyAgent: UVM agent for Moore FSM.

Creates and connects sequencer, driver, and monitor into a cohesive verification
unit. Implements the agent pattern to coordinate transaction flow from sequence
generation to DUT actuation and monitoring.
"""

from pyuvm import *
from MyDriver import MyDriver
from MySequencer import MySequencer
from MyMonitor import MyMonitor

class MyAgent(uvm_agent):
    """
    UVM agent: coordinates sequencer, driver, and monitor.
    
    Operation:
    - Creates sequencer (transaction coordination)
    - Creates driver (DUT input actuation) if agent is active
    - Creates monitor (DUT output observation) always
    - Connects driver to sequencer for transaction delivery
    """
    def __init__(self, name, parent, is_active=True):
        super().__init__(name, parent)
        self.sequencer=None
        self.is_active=is_active

    def build_phase(self):
        """
        Build Phase: Instantiate sequencer, driver (if active), and monitor.
        
        Creates the core agent components. Active mode includes driver for
        stimulus generation; passive mode only observes via monitor.
        """
        self.sequencer=MySequencer.create("sequencer", self)
        if self.is_active:
            self.driver=MyDriver.create("driver", self)
        self.monitor=MyMonitor.create("monitor", self)

    def connect_phase(self):
        """
        Connect Phase: Wire driver to sequencer if agent is active.
        
        Establishes TLM connection so driver can retrieve transactions
        from sequencer via get_next_item() calls.
        """
        if self.is_active:
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export)