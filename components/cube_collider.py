"""
A cube shaped collider for the physics engine.

"""
import numpy as np
from panda3d.bullet import BulletBoxShape
from panda3d.core import LVector3f, TransformState

from components.rigidbody import Rigidbody
from tools.envedit import helper
from tools.envedit.edenv_component import EComponent
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.wire_cube_gizmo import WireCubeGizmo
from tools.envedit.property_type import PropertyType
from tools.envedit.transform import Transform


class CubeCollider(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.cube_gizmo = None

    @staticmethod
    def get_properties():
        return {"center": PropertyType.VECTOR3,
                "size": PropertyType.VECTOR3}

    def on_gui_change(self):
        # Remove cube gizmo if it exists
        if self.cube_gizmo is not None:
            self.cube_gizmo.destroy()
            self.cube_gizmo = None

    def on_gui_change_selected(self):
        # Create cube gizmo if it doesn't exist
        if self.cube_gizmo is None:
            self.cube_gizmo = WireCubeGizmo()
            self.cube_gizmo.set_color((0, 1, 0, 1))

        # Transform cube
        cube_transform = Transform()
        cube_transform.set_scale(np.array([float(self.property_vals["size"][0]),
                                           float(self.property_vals["size"][1]),
                                           float(self.property_vals["size"][2])]))
        cube_transform.set_translation(np.array([float(self.property_vals["center"][0]),
                                                 float(self.property_vals["center"][1]),
                                                 float(self.property_vals["center"][2])]))
        self.cube_gizmo.set_world_matrix(self.node.transform.get_world_matrix().dot(cube_transform.get_mat()))

    def on_gui_remove(self):
        if self.cube_gizmo is not None:
            self.cube_gizmo.destroy()
            GizmoSystem.remove_gizmo(self.cube_gizmo)
            self.cube_gizmo = None

    def start(self):
        for component in self.node.data:
            if isinstance(component, Rigidbody):
                size = np.array([float(self.property_vals["size"][0]) / 2,
                                 float(self.property_vals["size"][1]) / 2,
                                 float(self.property_vals["size"][2]) / 2])
                shape = BulletBoxShape(helper.np_vec3_to_panda(size))
                center = LVector3f(float(self.property_vals["center"][0]),
                                   float(self.property_vals["center"][1]),
                                   float(self.property_vals["center"][2]))
                component.body_path.node().add_shape(shape, TransformState.make_pos(center))
