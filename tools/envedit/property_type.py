"""
The types that properties of a component can be represented by.

@author Ben Giacalone
"""
from enum import Enum, auto


class PropertyType(Enum):
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
