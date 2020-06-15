"""
A sphere shaped collider for the physics engine.

"""
import math

import numpy as np
from panda3d.bullet import BulletSphereShape
from panda3d.core import TransformState, LVector3f

from components.rigidbody import Rigidbody
from tools.envedit.edenv_component import EComponent
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.wire_circle_gizmo import WireCircleGizmo
from tools.envedit.property_type import PropertyType
from tools.envedit.transform import Transform


class SphereCollider(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.x_circle_gizmo = None
        self.y_circle_gizmo = None
        self.z_circle_gizmo = None

    @staticmethod
    def get_properties():
        return {"center": PropertyType.VECTOR3,
                "radius": PropertyType.FLOAT}

    def on_gui_change(self):
        # Remove circle gizmos if it exists
        if self.x_circle_gizmo is not None:
            self.x_circle_gizmo.destroy()
            self.x_circle_gizmo = None
            self.y_circle_gizmo.destroy()
            self.y_circle_gizmo = None
            self.z_circle_gizmo.destroy()
            self.z_circle_gizmo = None

    def on_gui_change_selected(self):
        # Create circle gizmo if it doesn't exist
        if self.x_circle_gizmo is None:
            self.x_circle_gizmo = WireCircleGizmo()
            self.x_circle_gizmo.set_color((0, 1, 0, 1))
            self.y_circle_gizmo = WireCircleGizmo()
            self.y_circle_gizmo.set_color((0, 1, 0, 1))
            self.z_circle_gizmo = WireCircleGizmo()
            self.z_circle_gizmo.set_color((0, 1, 0, 1))

        # Transform circles
        radius = float(self.property_vals["radius"])
        center_vector = np.array([float(self.property_vals["center"][0]),
                                  float(self.property_vals["center"][1]),
                                  float(self.property_vals["center"][2])])
        x_circle_transform = Transform()
        x_circle_transform.set_scale(np.array([radius, radius, radius]))
        x_circle_transform.set_translation(center_vector)
        self.x_circle_gizmo.set_world_matrix(self.node.transform.get_world_matrix().dot(x_circle_transform.get_mat()))

        y_circle_transform = Transform()
        y_circle_transform.set_scale(np.array([radius, radius, radius]))
        y_circle_transform.set_rotation(np.array([0, math.radians(90), 0]))
        y_circle_transform.set_translation(center_vector)
        self.y_circle_gizmo.set_world_matrix(self.node.transform.get_world_matrix().dot(y_circle_transform.get_mat()))

        z_circle_transform = Transform()
        z_circle_transform.set_scale(np.array([radius, radius, radius]))
        z_circle_transform.set_rotation(np.array([math.radians(90), 0, 0]))
        z_circle_transform.set_translation(center_vector)
        self.z_circle_gizmo.set_world_matrix(self.node.transform.get_world_matrix().dot(z_circle_transform.get_mat()))

    def on_gui_remove(self):
        if self.x_circle_gizmo is not None:
            self.x_circle_gizmo.destroy()
            self.y_circle_gizmo.destroy()
            self.z_circle_gizmo.destroy()

            GizmoSystem.remove_gizmo(self.x_circle_gizmo)
            GizmoSystem.remove_gizmo(self.y_circle_gizmo)
            GizmoSystem.remove_gizmo(self.z_circle_gizmo)

            self.x_circle_gizmo = None
            self.y_circle_gizmo = None
            self.z_circle_gizmo = None

    def start(self):
        for component in self.node.data:
            if isinstance(component, Rigidbody):
                radius = float(self.property_vals["radius"]) / 2
                shape = BulletSphereShape(radius)
                component.body_path.node().add_shape(shape, TransformState.make_pos(LVector3f(float(self.property_vals["center"][0]),
                                                                                              float(self.property_vals["center"][1]),
                                                                                              float(self.property_vals["center"][2]))))
