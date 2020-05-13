"""
Renders a mesh.

"""
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType


class MeshGraphic(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.mesh = None
        
    # Called by scene editor to get this component's properties
    @staticmethod
    def get_properties():
        return {"mesh": PropertyType.FILE}

    # Called when the scene starts
    def start(self, properties):
        self.mesh = properties["mesh"]
