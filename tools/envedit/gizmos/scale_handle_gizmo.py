"""
A handle gizmo for scaling.

@author Ben Giacalone
"""
import json
from os import path
from pathlib import Path

import numpy as np

from components.mesh_graphic import MeshGraphic
from tools.envedit import helper
from tools.envedit.envedit_data import EnveditData
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo
from tools.envedit.graph_node import GraphNode


class ScaleHandleGizmo(MeshGizmo):
    SCALE_X = 0
    SCALE_Y = 1
    SCALE_Z = 2

    # scale_axis: the axis to scale along
    def __init__(self, scale_axis):
        MeshGizmo.__init__(self)
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.start_mouse_axis_pos = np.array([0, 0, 0, 1])
        self.scale_callback = None
        self.scale_finished_callback = None
        self.component = None
        self.start_scale = np.array([1, 1, 1])
        self.scale_axis = scale_axis

        # Load handle mesh file
        handle_json = None
        handle_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/meshes/scale_handle.json"
        with open(handle_path, "r") as file:
            handle_json = json.load(file)

        # Generate mesh (renders on top of everything else)
        MeshGizmo.gen_geom(self, handle_json)
        self.get_geom().setColor(self.color)
        self.get_geom().setBin("fixed", 0)
        self.get_geom().setDepthTest(False)
        self.get_geom().setLightOff()

        # Define plane normal
        self.plane_normal = None
        self.handle_dir = None
        self.gen_plane_normal()

    # Sets arrow's color
    def set_color(self, color):
        self.color = color
        self.get_geom().setColor(self.color)

    def handle_left_pressed(self):
        # Get starting position of node and projected mouse
        node_world_pos = self.component.node.transform.get_world_translation()
        view_mouse_pos = np.array([GizmoSystem.gizmo_system.raw_mouse_x,
                                   GizmoSystem.gizmo_system.raw_mouse_y])
        start_mouse_world_pos = self.get_ray_plane_intersection(view_mouse_pos,
                                                                node_world_pos,
                                                                self.plane_normal)
        self.start_mouse_axis_pos = (self.handle_dir.dot(start_mouse_world_pos - node_world_pos) / self.handle_dir.dot(
            self.handle_dir)) * self.handle_dir
        self.start_scale = self.component.node.transform.get_world_scale()

        # Tell gizmo to start dragging
        GizmoSystem.set_drag(self)
        self.get_geom().setColor(self.color[0] - 0.2, self.color[1] - 0.2, self.color[2] - 0.2, self.color[3])

    def handle_left_released(self):
        self.get_geom().setColor(self.color)

    def handle_drag(self):
        # Get projected coordinates of new mouse
        node_world_pos = self.component.node.transform.get_world_translation()
        view_mouse_pos = np.array([GizmoSystem.gizmo_system.raw_mouse_x,
                                   GizmoSystem.gizmo_system.raw_mouse_y])
        new_mouse_world_pos = self.get_ray_plane_intersection(view_mouse_pos,
                                                              node_world_pos,
                                                              self.plane_normal)
        if new_mouse_world_pos is None or self.start_mouse_axis_pos is None:
            return

        # Create the scaling vector
        scale_vec = None
        new_mouse_axis_pos = (self.handle_dir.dot(new_mouse_world_pos - node_world_pos) / self.handle_dir.dot(
            self.handle_dir)) * self.handle_dir
        delta_scale = np.linalg.norm(new_mouse_axis_pos) - np.linalg.norm(self.start_mouse_axis_pos)
        if self.scale_axis == ScaleHandleGizmo.SCALE_X:
            scale_vec = np.array([delta_scale, 0, 0])
        elif self.scale_axis == ScaleHandleGizmo.SCALE_Y:
            scale_vec = np.array([0, delta_scale, 0])
        else:
            scale_vec = np.array([0, 0, delta_scale])
        if self.scale_callback is not None:
            self.scale_callback(self.component, self.start_scale + scale_vec)

    def handle_drag_stop(self):
        self.get_geom().setColor(self.color)
        if self.scale_finished_callback is not None:
            self.scale_finished_callback(self.component)

    # Returns the world space coordinate of a view space point
    # The world space coordinate is projected onto a 2D plane facing the camera
    def view_to_world(self, view_point):
        camera = GizmoSystem.gizmo_system.base.camera
        proj_mat = helper.panda_mat4_to_np(GizmoSystem.gizmo_system.base.camLens.getProjectionMat())
        cam_mat = np.linalg.inv(helper.panda_mat4_to_np(camera.getTransform().getMat()))
        view_to_world_mat = np.linalg.inv(cam_mat).dot(np.linalg.inv(proj_mat))
        world_point = view_to_world_mat.dot(np.array([view_point[0], view_point[1], -1, 1]))[:3]
        return world_point

    # Returns the world space intersection of a camera ray and a plane
    # The ray is generated from a view space coordinate
    # The plane is in world space
    def get_ray_plane_intersection(self, view_point, plane_center, plane_normal):
        # Convert screen point to ray in world space
        cam_pos = GizmoSystem.gizmo_system.base.camera.getTransform().getPos()
        ray_origin = np.array([cam_pos[0], cam_pos[1], cam_pos[2]])
        ray_dir = self.view_to_world(view_point) - ray_origin

        # Calculate intersection
        denom = ray_dir.dot(plane_normal)
        if abs(denom) < 0.001:
            return None
        else:
            multiplier = (plane_center - ray_origin).dot(plane_normal) / denom
            return ray_origin + ray_dir * multiplier

    # Generate the plane normal
    def gen_plane_normal(self):
        if self.component is not None:
            rot_mat = self.component.node.transform.get_rot_mat(self.component.node.transform.get_world_rotation())
            if self.scale_axis == ScaleHandleGizmo.SCALE_X:
                self.plane_normal = rot_mat.dot(np.array([0, 0, 1, 1]))[:3]
                self.handle_dir = rot_mat.dot(np.array([1, 0, 0, 1]))[:3]
            elif self.scale_axis == ScaleHandleGizmo.SCALE_Y:
                self.plane_normal = rot_mat.dot(np.array([0, 0, 1, 1]))[:3]
                self.handle_dir = rot_mat.dot(np.array([0, 1, 0, 1]))[:3]
            else:
                self.plane_normal = rot_mat.dot(np.array([1, 0, 0, 1]))[:3]
                self.handle_dir = rot_mat.dot(np.array([0, 0, 1, 1]))[:3]
