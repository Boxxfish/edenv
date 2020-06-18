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
from tools.envedit.gizmos.sphere_handle_gizmo import SphereHandleGizmo
from tools.envedit.gizmos.wire_cube_gizmo import WireCubeGizmo
from tools.envedit.property_type import PropertyType
from tools.envedit.transform import Transform
from tools.run.event import handler, send_event


class CubeCollider(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.cube_gizmo = None
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
                "size": PropertyType.VECTOR3}

    def on_gui_change(self):
        # Remove cube gizmo if it exists
        if self.cube_gizmo is not None:
            self.cube_gizmo.destroy()
            self.cube_gizmo = None

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
        # Create cube gizmo if it doesn't exist
        if self.cube_gizmo is None:
            self.cube_gizmo = WireCubeGizmo()
            self.cube_gizmo.set_color((0, 1, 0, 1))

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

        # Transform cube
        cube_transform = Transform()
        cube_transform.set_parent_matrix(self.node.transform.get_world_matrix())
        cube_transform.set_scale(np.array([float(self.property_vals["size"][0]),
                                           float(self.property_vals["size"][1]),
                                           float(self.property_vals["size"][2])]))
        cube_transform.set_translation(np.array([float(self.property_vals["center"][0]),
                                                 float(self.property_vals["center"][1]),
                                                 float(self.property_vals["center"][2])]))
        self.cube_gizmo.set_world_matrix(cube_transform.get_world_matrix())

        # Transform sphere handles
        master_mat = self.node.transform.get_world_matrix().dot(cube_transform.get_mat())
        x_min_transform = Transform()
        x_min_transform.set_scale(1 / (np.array([0.001, 0.001, 0.001]) + cube_transform.get_world_scale()))
        x_min_transform.set_translation(np.array([-0.5, 0, 0]))
        x_max_transform = Transform()
        x_max_transform.set_scale(1 / (np.array([0.001, 0.001, 0.001]) + cube_transform.get_world_scale()))
        x_max_transform.set_translation(np.array([0.5, 0, 0]))
        y_min_transform = Transform()
        y_min_transform.set_scale(1 / (np.array([0.001, 0.001, 0.001]) + cube_transform.get_world_scale()))
        y_min_transform.set_translation(np.array([0, -0.5, 0]))
        y_max_transform = Transform()
        y_max_transform.set_scale(1 / (np.array([0.001, 0.001, 0.001]) + cube_transform.get_world_scale()))
        y_max_transform.set_translation(np.array([0, 0.5, 0]))
        z_min_transform = Transform()
        z_min_transform.set_scale(1 / (np.array([0.001, 0.001, 0.001]) + cube_transform.get_world_scale()))
        z_min_transform.set_translation(np.array([0, 0, -0.5]))
        z_max_transform = Transform()
        z_max_transform.set_scale(1 / (np.array([0.001, 0.001, 0.001]) + cube_transform.get_world_scale()))
        z_max_transform.set_translation(np.array([0, 0, 0.5]))

        self.x_min_gizmo.set_world_matrix(master_mat.dot(x_min_transform.get_mat()))
        self.x_max_gizmo.set_world_matrix(master_mat.dot(x_max_transform.get_mat()))
        self.y_min_gizmo.set_world_matrix(master_mat.dot(y_min_transform.get_mat()))
        self.y_max_gizmo.set_world_matrix(master_mat.dot(y_max_transform.get_mat()))
        self.z_min_gizmo.set_world_matrix(master_mat.dot(z_min_transform.get_mat()))
        self.z_max_gizmo.set_world_matrix(master_mat.dot(z_max_transform.get_mat()))

    def on_gui_remove(self):
        if self.cube_gizmo is not None:
            self.cube_gizmo.destroy()
            GizmoSystem.remove_gizmo(self.cube_gizmo)
            self.cube_gizmo = None

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
                size = np.array([float(self.property_vals["size"][0]) / 2,
                                 float(self.property_vals["size"][1]) / 2,
                                 float(self.property_vals["size"][2]) / 2])
                shape = BulletBoxShape(helper.np_vec3_to_panda(size))
                center = LVector3f(float(self.property_vals["center"][0]),
                                   float(self.property_vals["center"][1]),
                                   float(self.property_vals["center"][2]))
                component.body_path.node().add_shape(shape, TransformState.make_pos(center))

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
            self.start_size = float(self.property_vals["size"][0])
            self.start_center = float(self.property_vals["center"][0])
        elif data == "x_max":
            self.start_size = float(self.property_vals["size"][0])
            self.start_center = float(self.property_vals["center"][0])
        elif data == "y_min":
            self.start_size = float(self.property_vals["size"][1])
            self.start_center = float(self.property_vals["center"][1])
        elif data == "y_max":
            self.start_size = float(self.property_vals["size"][1])
            self.start_center = float(self.property_vals["center"][1])
        elif data == "z_min":
            self.start_size = float(self.property_vals["size"][2])
            self.start_center = float(self.property_vals["center"][2])
        elif data == "z_max":
            self.start_size = float(self.property_vals["size"][2])
            self.start_center = float(self.property_vals["center"][2])

    # Handles a sphere handle dragging
    def handle_sphere_drag(self, drag_amount, data):
        if data == "x_min":
            self.property_vals["size"][0] = str(self.start_size - drag_amount)
            self.property_vals["center"][0] = str(self.start_center + drag_amount / 2)
        elif data == "x_max":
            self.property_vals["size"][0] = str(self.start_size + drag_amount)
            self.property_vals["center"][0] = str(self.start_center + drag_amount / 2)
        elif data == "y_min":
            self.property_vals["size"][1] = str(self.start_size - drag_amount)
            self.property_vals["center"][1] = str(self.start_center + drag_amount / 2)
        elif data == "y_max":
            self.property_vals["size"][1] = str(self.start_size + drag_amount)
            self.property_vals["center"][1] = str(self.start_center + drag_amount / 2)
        elif data == "z_min":
            self.property_vals["size"][2] = str(self.start_size - drag_amount)
            self.property_vals["center"][2] = str(self.start_center + drag_amount / 2)
        elif data == "z_max":
            self.property_vals["size"][2] = str(self.start_size + drag_amount)
            self.property_vals["center"][2] = str(self.start_center + drag_amount / 2)

        self.node.component_property_changed_selected()

    # Handles a sphere handle finished dragging
    def handle_sphere_finished(self, data):
        if self.component_update_callback is not None:
            self.component_update_callback("size")
            self.component_update_callback("center")
