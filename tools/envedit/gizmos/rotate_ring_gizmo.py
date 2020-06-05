"""
A ring gizmo for rotation.

@author Ben Giacalone
"""
import json
import math
from os import path
from pathlib import Path
import numpy as np
from math import cos, sin, atan2, asin
from components.mesh_graphic import MeshGraphic
from tools.envedit import helper
from tools.envedit.envedit_data import EnveditData
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo
from tools.envedit.graph_node import GraphNode
from tools.envedit.transform import Transform


class RotateRingGizmo(MeshGizmo):
    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    # axis: the axis the ring is aligned to
    def __init__(self, axis):
        MeshGizmo.__init__(self)
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.start_mouse_world_vec = np.array([0, 0, 0, 1])
        self.rotate_callback = None
        self.rotate_finished_callback = None
        self.component = None
        self.start_rot_mat = None
        self.axis = axis

        # Load ring mesh file
        ring_json = None
        ring_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/meshes/rotate_ring.json"
        with open(ring_path, "r") as file:
            ring_json = json.load(file)

        # Generate mesh (renders on top of everything else)
        MeshGizmo.gen_geom(self, ring_json)
        self.geom_path.setTag("shader type", "gizmo")
        self.get_geom().setColor(self.color)
        self.get_geom().setBin("fixed", 0)
        self.get_geom().setDepthTest(False)
        self.get_geom().setLightOff()

        # Define plane normal
        self.plane_normal = None
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
        plane_point = self.get_ray_plane_intersection(view_mouse_pos,
                                                      self.component.node.transform.get_world_translation(),
                                                      self.plane_normal)
        if plane_point is None or np.linalg.norm(plane_point) < 0.001:
            return
        self.start_mouse_world_vec = (plane_point - node_world_pos) / np.linalg.norm(plane_point - node_world_pos)
        self.start_rot_mat = self.component.node.transform.get_rot_mat(self.component.node.transform.get_rotation())

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
        plane_point = self.get_ray_plane_intersection(view_mouse_pos,
                                                      node_world_pos,
                                                      self.plane_normal)
        if plane_point is None or np.linalg.norm(plane_point) < 0.001:
            return
        new_mouse_world_vec = (plane_point - node_world_pos) / np.linalg.norm(plane_point - node_world_pos)
        if new_mouse_world_vec is None or self.start_mouse_world_vec is None:
            return

        # Find delta angle
        angle_sin = self.plane_normal.dot(np.cross(self.start_mouse_world_vec, new_mouse_world_vec))
        angle_cos = new_mouse_world_vec.dot(self.start_mouse_world_vec)
        delta_angle = math.atan2(angle_sin, angle_cos)

        # Get euler rotation vector
        new_transform = Transform()
        if self.axis == RotateRingGizmo.AXIS_X:
            new_transform.set_rotation(np.array([delta_angle, 0, 0]))
        elif self.axis == RotateRingGizmo.AXIS_Y:
            new_transform.set_rotation(np.array([0, delta_angle, 0]))
        else:
            new_transform.set_rotation(np.array([0, 0, delta_angle]))
        final_transform = Transform()
        final_transform.set_matrix(self.start_rot_mat.dot(new_transform.get_mat()))
        if self.rotate_callback is not None:
            self.rotate_callback(self.component, final_transform.get_rotation())

    def handle_drag_stop(self):
        self.get_geom().setColor(self.color)
        if self.rotate_finished_callback is not None:
            self.rotate_finished_callback(self.component)

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
            if self.axis == RotateRingGizmo.AXIS_X:
                self.plane_normal = rot_mat.dot(np.array([1, 0, 0, 1]))[:3]
            elif self.axis == RotateRingGizmo.AXIS_Y:
                self.plane_normal = rot_mat.dot(np.array([0, 1, 0, 1]))[:3]
            else:
                self.plane_normal = rot_mat.dot(np.array([0, 0, 1, 1]))[:3]
