"""
AlterCycle: A specialized data structure for handling alternating binary states in cyclic sequences.

This package provides a data structure optimized for problems where:
1. Data naturally alternates between two states
2. Pattern detection needs to consider state alternation
3. Cyclic relationships are inherent to the data
4. State transitions follow a strict alternating pattern
"""

from .node import AlterNode
from .linked_list import AlterCycle

__version__ = "1.0.0"
__all__ = ['AlterNode', 'AlterCycle']
