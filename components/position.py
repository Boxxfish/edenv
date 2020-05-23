"""
Represents the world space position of this model.

"""
import json
import math
from os import path
from pathlib import Path

import numpy as np
from panda3d.core import ShadeModelAttrib, Filename, Shader

from tools.envedit.edenv_component import EComponent
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo
from tools.envedit.gizmos.translate_arrow_gizmo import TranslateArrowGizmo
from tools.envedit.property_type import PropertyType
from tools.envedit.transform import Transform


class Position(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.x_arrow_gizmo = None
        self.y_arrow_gizmo = None
        self.z_arrow_gizmo = None

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
        # Set transform properties
        self.node.transform.set_translation(np.array([float(properties["pos_x"]),
                                                      float(properties["pos_y"]),
                                                      float(properties["pos_z"])]))
        self.node.transform.set_rotation(np.array([math.radians(float(properties["rot_x"])),
                                                   math.radians(float(properties["rot_y"])),
                                                   math.radians(float(properties["rot_z"]))]))
        self.node.transform.set_scale(np.array([float(properties["scale_x"]),
                                                float(properties["scale_y"]),
                                                float(properties["scale_z"])]))

        # Destroy previous arrows
        if hasattr(self, "x_arrow_gizmo"):
            GizmoSystem.remove_gizmo(self.x_arrow_gizmo)
            self.x_arrow_gizmo.destroy()
            GizmoSystem.remove_gizmo(self.y_arrow_gizmo)
            self.y_arrow_gizmo.destroy()
            GizmoSystem.remove_gizmo(self.z_arrow_gizmo)
            self.z_arrow_gizmo.destroy()

        # Create arrows
        self.x_arrow_gizmo = TranslateArrowGizmo()
        self.x_arrow_gizmo.set_color((0.8, 0.2, 0.2, 1))
        GizmoSystem.add_gizmo(self.x_arrow_gizmo)
        x_transform = Transform()
        x_transform.set_scale((0.1, 0.1, 0.1))
        x_transform.set_translation(self.node.transform.trans + (1, 0, 0))
        x_transform.set_rotation((0, math.radians(90), 0))
        self.x_arrow_gizmo.set_world_matrix(x_transform.get_mat())

        self.y_arrow_gizmo = TranslateArrowGizmo()
        self.y_arrow_gizmo.set_color((0.2, 0.8, 0.2, 1))
        GizmoSystem.add_gizmo(self.y_arrow_gizmo)
        y_transform = Transform()
        y_transform.set_scale((0.1, 0.1, 0.1))
        y_transform.set_translation(self.node.transform.trans + (0, 1, 0))
        y_transform.set_rotation((math.radians(-90), 0, 0))
        self.y_arrow_gizmo.set_world_matrix(y_transform.get_mat())

        self.z_arrow_gizmo = TranslateArrowGizmo()
        self.z_arrow_gizmo.set_color((0.2, 0.2, 0.8, 1))
        GizmoSystem.add_gizmo(self.z_arrow_gizmo)
        z_transform = Transform()
        z_transform.set_scale((0.1, 0.1, 0.1))
        z_transform.set_translation(self.node.transform.trans + (0, 0, 1))
        self.z_arrow_gizmo.set_world_matrix(z_transform.get_mat())

    def on_gui_remove(self, properties):
        pass

    # Called when the scene starts
    def start(self, properties):
        pass
