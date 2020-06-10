"""
Point constraint for the physics system.

"""
from tools.envedit.edenv_component import EComponent


class PointConstraint(EComponent):

    def __init__(self):
        EComponent.__init__(self)

    @staticmethod
    def get_properties():
        return {}

    def update(self):
        # TODO: Integrate with physics system
        pass