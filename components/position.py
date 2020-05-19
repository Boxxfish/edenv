"""
Represents the world space position of this model.

"""
import math

import numpy as np
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType


class Position(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        
    # Called by scene editor to get this component's properties
    @staticmethod
    def get_properties():
        return {"pos_x": PropertyType.FLOAT,
                "pos_y": PropertyType.FLOAT,
                "pos_z": PropertyType.FLOAT,
                "rot_x": PropertyType.FLOAT,
                "rot_y": PropertyType.FLOAT,
                "rot_z": PropertyType.FLOAT,
                "scale_x": PropertyType.FLOAT,
                "scale_y": PropertyType.FLOAT,
                "scale_z": PropertyType.FLOAT}

    # Called when component property is changed
    def on_gui_change(self, properties):
        self.node.transform.set_translation(np.array([float(properties["pos_x"]),
                                                      float(properties["pos_y"]),
                                                      float(properties["pos_z"])]))
        self.node.transform.set_rotation(np.array([math.radians(float(properties["rot_x"])),
                                                   math.radians(float(properties["rot_y"])),
                                                   math.radians(float(properties["rot_z"]))]))
        self.node.transform.set_scale(np.array([float(properties["scale_x"]),
                                                float(properties["scale_y"]),
                                                float(properties["scale_z"])]))

    # Called when the scene starts
    def start(self, properties):
        pass
