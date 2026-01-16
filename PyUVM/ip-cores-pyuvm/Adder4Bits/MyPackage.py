

"""
MyPackage: Aggregates all UVM components for 4-bit Adder verification.

Provides single import point consolidating all testbench classes and packet
definitions, simplifying top-level imports.
"""

from Pkt import Pkt
from MySequence import MySequence
from MySequencer import MySequencer
from MyDriver import MyDriver
from MyMonitor import MyMonitor
from MyAgent import MyAgent
from MyEnv import MyEnv
from MyScoreboard import MyScoreboard
from Adder4BitsWrapper import Adder4BitsWrapper
from MyCoverage import MyCoverage

__all__ = [
    "Pkt",
    "MySequence",
    "MySequencer",
    "MyDriver",
    "MyMonitor",
    "MyAgent",
    "MyEnv",
    "MyScoreboard",
    "Adder4BitsWrapper",
    "MyCoverage"
]