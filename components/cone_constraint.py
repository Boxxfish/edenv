"""
Cone constraint for the physics engine.

"""
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType


class ConeConstraint(EComponent):

    def __init__(self):
        EComponent.__init__(self)

    @staticmethod
    def get_properties():
        return {"axis": PropertyType.VECTOR3,
                "radius": PropertyType.FLOAT}

    def update(self):
        # TODO: Integrate with physics system
        pass