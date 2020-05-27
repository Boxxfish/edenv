"""
Represents the world space position of this model.

"""
import math
import numpy as np
from tools.envedit.edenv_component import EComponent
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.rotate_ring_gizmo import RotateRingGizmo
from tools.envedit.gizmos.translate_arrow_gizmo import TranslateArrowGizmo
from tools.envedit.property_type import PropertyType
from tools.envedit.transform import Transform


class Position(EComponent):

    def __init__(self):
        EComponent.__init__(self)

        self.x_arrow_gizmo = None
        self.y_arrow_gizmo = None
        self.z_arrow_gizmo = None

        self.x_ring_gizmo = None
        self.y_ring_gizmo = None
        self.z_ring_gizmo = None

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

    # Called when component property is changed and the component isn't selected
    def on_gui_change(self):
        # Remove translation gizmos
        if self.x_arrow_gizmo is not None:
            GizmoSystem.remove_gizmo(self.x_arrow_gizmo)
            self.x_arrow_gizmo.destroy()
            self.x_arrow_gizmo = None

            GizmoSystem.remove_gizmo(self.y_arrow_gizmo)
            self.y_arrow_gizmo.destroy()
            self.y_arrow_gizmo = None

            GizmoSystem.remove_gizmo(self.z_arrow_gizmo)
            self.z_arrow_gizmo.destroy()
            self.z_arrow_gizmo = None

        # Remove rotation gizmos
        if self.x_ring_gizmo is not None:
            GizmoSystem.remove_gizmo(self.x_ring_gizmo)
            self.x_ring_gizmo.destroy()
            self.x_ring_gizmo = None

            GizmoSystem.remove_gizmo(self.y_ring_gizmo)
            self.y_ring_gizmo.destroy()
            self.y_ring_gizmo = None

            GizmoSystem.remove_gizmo(self.z_ring_gizmo)
            self.z_ring_gizmo.destroy()
            self.z_ring_gizmo = None

    # Called when component property is changed and the component is selected
    def on_gui_change_selected(self):
        # Set transform properties
        self.node.transform.set_translation(np.array([float(self.property_vals["pos_x"]),
                                                      float(self.property_vals["pos_y"]),
                                                      float(self.property_vals["pos_z"])]))
        self.node.transform.set_rotation(np.array([math.radians(float(self.property_vals["rot_x"])),
                                                   math.radians(float(self.property_vals["rot_y"])),
                                                   math.radians(float(self.property_vals["rot_z"]))]))
        self.node.transform.set_scale(np.array([float(self.property_vals["scale_x"]),
                                                float(self.property_vals["scale_y"]),
                                                float(self.property_vals["scale_z"])]))

        # Create arrows
        if self.x_arrow_gizmo is None:
            self.x_arrow_gizmo = TranslateArrowGizmo(TranslateArrowGizmo.DIR_X)
            self.x_arrow_gizmo.set_color((0.8, 0.2, 0.2, 1))
            GizmoSystem.add_gizmo(self.x_arrow_gizmo)
            self.x_arrow_gizmo.component = self
            self.x_arrow_gizmo.translate_callback = Position.handle_translation
            self.x_arrow_gizmo.translate_finished_callback = Position.handle_finished_translation

            self.y_arrow_gizmo = TranslateArrowGizmo(TranslateArrowGizmo.DIR_Y)
            self.y_arrow_gizmo.set_color((0.2, 0.8, 0.2, 1))
            GizmoSystem.add_gizmo(self.y_arrow_gizmo)
            self.y_arrow_gizmo.component = self
            self.y_arrow_gizmo.translate_callback = Position.handle_translation
            self.y_arrow_gizmo.translate_finished_callback = Position.handle_finished_translation

            self.z_arrow_gizmo = TranslateArrowGizmo(TranslateArrowGizmo.DIR_Z)
            self.z_arrow_gizmo.set_color((0.2, 0.2, 0.8, 1))
            GizmoSystem.add_gizmo(self.z_arrow_gizmo)
            self.z_arrow_gizmo.component = self
            self.z_arrow_gizmo.translate_callback = Position.handle_translation
            self.z_arrow_gizmo.translate_finished_callback = Position.handle_finished_translation

        # Create rings
        if self.x_ring_gizmo is None:
            self.x_ring_gizmo = RotateRingGizmo(RotateRingGizmo.AXIS_X)
            self.x_ring_gizmo.set_color((0.8, 0.2, 0.2, 1))
            GizmoSystem.add_gizmo(self.x_ring_gizmo)
            self.x_ring_gizmo.component = self
            self.x_ring_gizmo.rotate_callback = Position.handle_rotation
            self.x_ring_gizmo.rotate_finished_callback = Position.handle_finished_rotation

            self.y_ring_gizmo = RotateRingGizmo(RotateRingGizmo.AXIS_Y)
            self.y_ring_gizmo.set_color((0.2, 0.8, 0.2, 1))
            GizmoSystem.add_gizmo(self.y_ring_gizmo)
            self.y_ring_gizmo.component = self
            self.y_ring_gizmo.rotate_callback = Position.handle_rotation
            self.y_ring_gizmo.rotate_finished_callback = Position.handle_finished_rotation

            self.z_ring_gizmo = RotateRingGizmo(RotateRingGizmo.AXIS_Z)
            self.z_ring_gizmo.set_color((0.2, 0.2, 0.8, 1))
            GizmoSystem.add_gizmo(self.z_ring_gizmo)
            self.z_ring_gizmo.component = self
            self.z_ring_gizmo.rotate_callback = Position.handle_rotation
            self.z_ring_gizmo.rotate_finished_callback = Position.handle_finished_rotation

        node_world_pos = self.node.transform.get_world_translation()

        # Set arrow transforms
        x_transform = Transform()
        x_transform.set_scale((0.1, 0.1, 0.1))
        x_transform.set_translation((node_world_pos[0] + 1, node_world_pos[1], node_world_pos[2]))
        x_transform.set_rotation((0, math.radians(90), 0))
        self.x_arrow_gizmo.set_world_matrix(x_transform.get_mat())

        y_transform = Transform()
        y_transform.set_scale((0.1, 0.1, 0.1))
        y_transform.set_translation((node_world_pos[0], node_world_pos[1] + 1, node_world_pos[2]))
        y_transform.set_rotation((math.radians(-90), 0, 0))
        self.y_arrow_gizmo.set_world_matrix(y_transform.get_mat())

        z_transform = Transform()
        z_transform.set_scale((0.1, 0.1, 0.1))
        z_transform.set_translation((node_world_pos[0], node_world_pos[1], node_world_pos[2] + 1))
        self.z_arrow_gizmo.set_world_matrix(z_transform.get_mat())

        # Set rotation transforms
        x_rot_transform = Transform()
        x_rot_transform.set_translation(node_world_pos)
        x_rot_transform.set_rotation((0, math.radians(90), 0))
        self.x_ring_gizmo.set_world_matrix(x_rot_transform.get_mat())

        y_rot_transform = Transform()
        y_rot_transform.set_translation(node_world_pos)
        y_rot_transform.set_rotation((math.radians(90), 0, 0))
        self.y_ring_gizmo.set_world_matrix(y_rot_transform.get_mat())

        z_rot_transform = Transform()
        z_rot_transform.set_translation(node_world_pos)
        self.z_ring_gizmo.set_world_matrix(z_rot_transform.get_mat())

    def on_gui_remove(self):
        # Remove translation gizmos
        if self.x_arrow_gizmo is not None:
            GizmoSystem.remove_gizmo(self.x_arrow_gizmo)
            self.x_arrow_gizmo.destroy()
            self.x_arrow_gizmo = None

            GizmoSystem.remove_gizmo(self.y_arrow_gizmo)
            self.y_arrow_gizmo.destroy()
            self.y_arrow_gizmo = None

            GizmoSystem.remove_gizmo(self.z_arrow_gizmo)
            self.z_arrow_gizmo.destroy()
            self.z_arrow_gizmo = None

        # Remove rotation gizmos
        if self.x_ring_gizmo is not None:
            GizmoSystem.remove_gizmo(self.x_ring_gizmo)
            self.x_ring_gizmo.destroy()
            self.x_ring_gizmo = None

            GizmoSystem.remove_gizmo(self.y_ring_gizmo)
            self.y_ring_gizmo.destroy()
            self.y_ring_gizmo = None

            GizmoSystem.remove_gizmo(self.z_ring_gizmo)
            self.z_ring_gizmo.destroy()
            self.z_ring_gizmo = None

    def handle_translation(self, new_pos):
        # Update transform
        self.node.transform.set_world_translation(new_pos)

        # Set position component's properties
        self.property_vals["pos_x"] = str(self.node.transform.trans[0])
        self.property_vals["pos_y"] = str(self.node.transform.trans[1])
        self.property_vals["pos_z"] = str(self.node.transform.trans[2])

        self.node.component_property_changed_selected()

    def handle_finished_translation(self):
        if self.component_update_callback is not None:
            self.component_update_callback("pos_x")
            self.component_update_callback("pos_y")
            self.component_update_callback("pos_z")

    def handle_rotation(self, new_rot):
        # Update transform
        self.node.transform.set_rotation(new_rot)

        # Set position component's properties
        self.property_vals["rot_x"] = str(math.degrees(self.node.transform.rot[0]))
        self.property_vals["rot_y"] = str(math.degrees(self.node.transform.rot[1]))
        self.property_vals["rot_z"] = str(math.degrees(self.node.transform.rot[2]))

        self.node.component_property_changed_selected()

    def handle_finished_rotation(self):
        if self.component_update_callback is not None:
            self.component_update_callback("rot_x")
            self.component_update_callback("rot_y")
            self.component_update_callback("rot_z")

    # Called when the scene starts
    def start(self, properties):
        pass
