"""
Represents the world space position of this model.

"""
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType


class Position(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.x = 0
        self.y = 0
        self.z = 0
        
    # Called by scene editor to get this component's properties
    @staticmethod
    def get_properties():
        return {"x": PropertyType.FLOAT, "y": PropertyType.FLOAT, "z": PropertyType.FLOAT}

    # Called when the scene starts
    def start(self, properties):
        self.x = properties["x"]
        self.y = properties["y"]
        self.z = properties["z"]
