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
from tools.envedit.gizmos.sphere_handle_gizmo import SphereHandleGizmo
from tools.envedit.gizmos.wire_circle_gizmo import WireCircleGizmo
from tools.envedit.property_type import PropertyType
from tools.envedit.transform import Transform
from tools.run.event import handler, send_event


class SphereCollider(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.x_circle_gizmo = None
        self.y_circle_gizmo = None
        self.z_circle_gizmo = None

        self.x_min_gizmo = None
        self.x_max_gizmo = None
        self.y_min_gizmo = None
        self.y_max_gizmo = None
        self.z_min_gizmo = None
        self.z_max_gizmo = None

        self.start_size = 0
        self.start_center = 0

        self.rigidbody_component = None
        self.touching = []

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

            self.x_min_gizmo.destroy()
            self.x_max_gizmo.destroy()
            self.y_min_gizmo.destroy()
            self.y_max_gizmo.destroy()
            self.z_min_gizmo.destroy()
            self.z_max_gizmo.destroy()

            self.x_min_gizmo = None
            self.x_max_gizmo = None
            self.y_min_gizmo = None
            self.y_max_gizmo = None
            self.z_min_gizmo = None
            self.z_max_gizmo = None

    def on_gui_change_selected(self):
        # Create circle gizmo if it doesn't exist
        if self.x_circle_gizmo is None:
            self.x_circle_gizmo = WireCircleGizmo()
            self.x_circle_gizmo.set_color((0, 1, 0, 1))
            self.y_circle_gizmo = WireCircleGizmo()
            self.y_circle_gizmo.set_color((0, 1, 0, 1))
            self.z_circle_gizmo = WireCircleGizmo()
            self.z_circle_gizmo.set_color((0, 1, 0, 1))

            self.x_min_gizmo = SphereHandleGizmo(np.array([1, 0, 0]))
            self.x_max_gizmo = SphereHandleGizmo(np.array([1, 0, 0]))
            self.y_min_gizmo = SphereHandleGizmo(np.array([0, 1, 0]))
            self.y_max_gizmo = SphereHandleGizmo(np.array([0, 1, 0]))
            self.z_min_gizmo = SphereHandleGizmo(np.array([0, 0, 1]))
            self.z_max_gizmo = SphereHandleGizmo(np.array([0, 0, 1]))

            self.x_min_gizmo.component = self
            self.x_max_gizmo.component = self
            self.y_min_gizmo.component = self
            self.y_max_gizmo.component = self
            self.z_min_gizmo.component = self
            self.z_max_gizmo.component = self

            self.x_min_gizmo.translate_callback = self.handle_sphere_drag
            self.x_max_gizmo.translate_callback = self.handle_sphere_drag
            self.y_min_gizmo.translate_callback = self.handle_sphere_drag
            self.y_max_gizmo.translate_callback = self.handle_sphere_drag
            self.z_min_gizmo.translate_callback = self.handle_sphere_drag
            self.z_max_gizmo.translate_callback = self.handle_sphere_drag

            self.x_min_gizmo.start_translate_callback = self.handle_sphere_selected
            self.x_max_gizmo.start_translate_callback = self.handle_sphere_selected
            self.y_min_gizmo.start_translate_callback = self.handle_sphere_selected
            self.y_max_gizmo.start_translate_callback = self.handle_sphere_selected
            self.z_min_gizmo.start_translate_callback = self.handle_sphere_selected
            self.z_max_gizmo.start_translate_callback = self.handle_sphere_selected

            self.x_min_gizmo.translate_finished_callback = self.handle_sphere_finished
            self.x_max_gizmo.translate_finished_callback = self.handle_sphere_finished
            self.y_min_gizmo.translate_finished_callback = self.handle_sphere_finished
            self.y_max_gizmo.translate_finished_callback = self.handle_sphere_finished
            self.z_min_gizmo.translate_finished_callback = self.handle_sphere_finished
            self.z_max_gizmo.translate_finished_callback = self.handle_sphere_finished

            self.x_min_gizmo.data = "x_min"
            self.x_max_gizmo.data = "x_max"
            self.y_min_gizmo.data = "y_min"
            self.y_max_gizmo.data = "y_max"
            self.z_min_gizmo.data = "z_min"
            self.z_max_gizmo.data = "z_max"

            GizmoSystem.add_gizmo(self.x_min_gizmo)
            GizmoSystem.add_gizmo(self.x_max_gizmo)
            GizmoSystem.add_gizmo(self.y_min_gizmo)
            GizmoSystem.add_gizmo(self.y_max_gizmo)
            GizmoSystem.add_gizmo(self.z_min_gizmo)
            GizmoSystem.add_gizmo(self.z_max_gizmo)

        # Transform circles
        world_scale = self.node.transform.get_world_scale()
        avg_scale = (world_scale[0] + world_scale[1] + world_scale[2]) / 3
        radius = float(self.property_vals["radius"]) * avg_scale + 0.001
        center_vector = np.array([float(self.property_vals["center"][0]),
                                  float(self.property_vals["center"][1]),
                                  float(self.property_vals["center"][2])])
        master_transform = Transform()
        master_transform.set_translation(self.node.transform.get_world_translation() + center_vector)
        master_transform.set_rotation(self.node.transform.get_world_rotation())

        x_circle_transform = Transform()
        x_circle_transform.set_parent_matrix(master_transform.get_mat())
        x_circle_transform.set_scale(np.array([radius, radius, radius]))
        x_circle_transform.set_rotation(np.array([math.radians(90), 0, 0]))
        self.x_circle_gizmo.set_world_matrix(x_circle_transform.get_world_matrix())

        y_circle_transform = Transform()
        y_circle_transform.set_parent_matrix(master_transform.get_mat())
        y_circle_transform.set_scale(np.array([radius, radius, radius]))
        y_circle_transform.set_rotation(np.array([0, math.radians(90), 0]))
        self.y_circle_gizmo.set_world_matrix(y_circle_transform.get_world_matrix())

        z_circle_transform = Transform()
        z_circle_transform.set_parent_matrix(master_transform.get_mat())
        z_circle_transform.set_scale(np.array([radius, radius, radius]))
        self.z_circle_gizmo.set_world_matrix(z_circle_transform.get_world_matrix())

        # Transform sphere handles
        x_min_transform = Transform()
        x_min_transform.set_translation(np.array([-0.5, 0, 0]) * np.array([radius, radius, radius]))
        x_max_transform = Transform()
        x_max_transform.set_translation(np.array([0.5, 0, 0]) * np.array([radius, radius, radius]))
        y_min_transform = Transform()
        y_min_transform.set_translation(np.array([0, -0.5, 0]) * np.array([radius, radius, radius]))
        y_max_transform = Transform()
        y_max_transform.set_translation(np.array([0, 0.5, 0]) * np.array([radius, radius, radius]))
        z_min_transform = Transform()
        z_min_transform.set_translation(np.array([0, 0, -0.5]) * np.array([radius, radius, radius]))
        z_max_transform = Transform()
        z_max_transform.set_translation(np.array([0, 0, 0.5]) * np.array([radius, radius, radius]))

        self.x_min_gizmo.set_world_matrix(master_transform.get_mat().dot(x_min_transform.get_mat()))
        self.x_max_gizmo.set_world_matrix(master_transform.get_mat().dot(x_max_transform.get_mat()))
        self.y_min_gizmo.set_world_matrix(master_transform.get_mat().dot(y_min_transform.get_mat()))
        self.y_max_gizmo.set_world_matrix(master_transform.get_mat().dot(y_max_transform.get_mat()))
        self.z_min_gizmo.set_world_matrix(master_transform.get_mat().dot(z_min_transform.get_mat()))
        self.z_max_gizmo.set_world_matrix(master_transform.get_mat().dot(z_max_transform.get_mat()))

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

            self.x_min_gizmo.destroy()
            self.x_max_gizmo.destroy()
            self.y_min_gizmo.destroy()
            self.y_max_gizmo.destroy()
            self.z_min_gizmo.destroy()
            self.z_max_gizmo.destroy()

            GizmoSystem.remove_gizmo(self.x_min_gizmo)
            GizmoSystem.remove_gizmo(self.x_max_gizmo)
            GizmoSystem.remove_gizmo(self.y_min_gizmo)
            GizmoSystem.remove_gizmo(self.y_max_gizmo)
            GizmoSystem.remove_gizmo(self.z_min_gizmo)
            GizmoSystem.remove_gizmo(self.z_max_gizmo)

            self.x_min_gizmo = None
            self.x_max_gizmo = None
            self.y_min_gizmo = None
            self.y_max_gizmo = None
            self.z_min_gizmo = None
            self.z_max_gizmo = None

    def start(self):
        for component in self.node.data:
            if isinstance(component, Rigidbody):
                self.rigidbody_component = component
                radius = float(self.property_vals["radius"]) / 2
                shape = BulletSphereShape(radius)
                component.body_path.node().add_shape(shape, TransformState.make_pos(LVector3f(float(self.property_vals["center"][0]),
                                                                                              float(self.property_vals["center"][1]),
                                                                                              float(self.property_vals["center"][2]))))

    @handler()
    def handle_update(self):
        result = self.physics.physics_world.contactTest(self.rigidbody_component.body_path.node())
        touching = []

        for contact in result.getContacts():
            id_1 = contact.getNode0().name[:-11]
            id_2 = contact.getNode1().name[:-11]
            touching.append(id_2)

            # Check if entered this frame
            if id_2 not in self.touching:
                send_event("main", "collision_enter", id_1, id_2)

        # Check if exited this frame
        for id in self.touching:
            if id not in touching:
                send_event("main", "collision_exit", self.node.id, id)

        self.touching = touching

    # Handles a sphere being selected
    def handle_sphere_selected(self, data):
        if data == "x_min":
            self.start_size = float(self.property_vals["radius"])
            self.start_center = float(self.property_vals["center"][0])
        elif data == "x_max":
            self.start_size = float(self.property_vals["radius"])
            self.start_center = float(self.property_vals["center"][0])
        elif data == "y_min":
            self.start_size = float(self.property_vals["radius"])
            self.start_center = float(self.property_vals["center"][1])
        elif data == "y_max":
            self.start_size = float(self.property_vals["radius"])
            self.start_center = float(self.property_vals["center"][1])
        elif data == "z_min":
            self.start_size = float(self.property_vals["radius"])
            self.start_center = float(self.property_vals["center"][2])
        elif data == "z_max":
            self.start_size = float(self.property_vals["radius"])
            self.start_center = float(self.property_vals["center"][2])

    # Handles a sphere handle dragging
    def handle_sphere_drag(self, drag_amount, data):
        if data == "x_min":
            self.property_vals["radius"] = str(self.start_size - drag_amount)
            self.property_vals["center"][0] = str(self.start_center + drag_amount / 2)
        elif data == "x_max":
            self.property_vals["radius"] = str(self.start_size + drag_amount)
            self.property_vals["center"][0] = str(self.start_center + drag_amount / 2)
        elif data == "y_min":
            self.property_vals["radius"] = str(self.start_size - drag_amount)
            self.property_vals["center"][1] = str(self.start_center + drag_amount / 2)
        elif data == "y_max":
            self.property_vals["radius"] = str(self.start_size + drag_amount)
            self.property_vals["center"][1] = str(self.start_center + drag_amount / 2)
        elif data == "z_min":
            self.property_vals["radius"] = str(self.start_size - drag_amount)
            self.property_vals["center"][2] = str(self.start_center + drag_amount / 2)
        elif data == "z_max":
            self.property_vals["radius"] = str(self.start_size + drag_amount)
            self.property_vals["center"][2] = str(self.start_center + drag_amount / 2)

        self.node.component_property_changed_selected()

    # Handles a sphere handle finished dragging
    def handle_sphere_finished(self, data):
        if self.component_update_callback is not None:
            self.component_update_callback("radius")
            self.component_update_callback("center")
