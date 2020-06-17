"""
A sample component.

"""
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType
from tools.run.event import handler


class SampleComponent(EComponent):

    def __init__(self):
        EComponent.__init__(self)

    @staticmethod
    def get_properties():
        # Define properties here
        # Properties can be accessed through self.property_vals
        return {"sample_property": PropertyType.STRING}

    # Runs once when the scene loads
    def start(self):
        pass
  
    # Updates every frame
    @handler()
    def handle_update(self):
        pass
