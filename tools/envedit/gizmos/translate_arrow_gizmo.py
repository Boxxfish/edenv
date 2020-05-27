"""
An arrow gizmo for translation.

@author Ben Giacalone
"""
import json
import math
from os import path
from pathlib import Path

import numpy as np
from panda3d.core import Filename, Shader, LVector4f

from components.mesh_graphic import MeshGraphic
from tools.envedit import helper
from tools.envedit.envedit_data import EnveditData
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo
from tools.envedit.graph_node import GraphNode
from tools.envedit.transform import Transform


class TranslateArrowGizmo(MeshGizmo):
    DIR_X = 0
    DIR_Y = 1
    DIR_Z = 2

    # direction: the direction in world space the arrow points
    def __init__(self, direction):
        MeshGizmo.__init__(self)
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.start_mouse_world_pos = np.array([0, 0, 0, 1])
        self.translate_callback = None
        self.translate_finished_callback = None
        self.component = None
        self.start_pos = np.array([0, 0, 0])
        self.direction = direction

        # Load arrow mesh file
        arrow_json = None
        arrow_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/meshes/translate_arrow.json"
        with open(arrow_path, "r") as file:
            arrow_json = json.load(file)

        # Generate mesh (renders on top of everything else
        MeshGizmo.gen_geom(self, arrow_json)
        self.get_geom().setColor(self.color)
        self.get_geom().setBin("fixed", 0)
        self.get_geom().setDepthTest(False)
        self.get_geom().setLightOff()

        # Define plane normal
        self.plane_normal = None
        if self.direction == TranslateArrowGizmo.DIR_X:
            self.plane_normal = np.array([0, 0, 1])
        elif self.direction == TranslateArrowGizmo.DIR_Y:
            self.plane_normal = np.array([0, 0, 1])
        else:
            self.plane_normal = np.array([1, 0, 0])

    # Sets arrow's color
    def set_color(self, color):
        self.color = color
        self.get_geom().setColor(self.color)

    def handle_left_pressed(self):
        # Get starting position of node and projected mouse
        view_mouse_pos = np.array([GizmoSystem.gizmo_system.raw_mouse_x,
                                   GizmoSystem.gizmo_system.raw_mouse_y])
        self.start_mouse_world_pos = self.get_ray_plane_intersection(view_mouse_pos,
                                                                     self.component.node.transform.get_world_translation(),
                                                                     self.plane_normal)
        self.start_pos = self.component.node.transform.get_world_translation()

        # Tell gizmo to start dragging
        GizmoSystem.set_drag(self)
        self.get_geom().setColor(self.color[0] - 0.2, self.color[1] - 0.2, self.color[2] - 0.2, self.color[3])

    def handle_left_released(self):
        self.get_geom().setColor(self.color)

    def handle_drag(self):
        # Get projected coordinates of new mouse
        view_mouse_pos = np.array([GizmoSystem.gizmo_system.raw_mouse_x,
                                   GizmoSystem.gizmo_system.raw_mouse_y])
        new_mouse_world_pos = self.get_ray_plane_intersection(view_mouse_pos,
                                                              self.component.node.transform.get_world_translation(),
                                                              self.plane_normal)
        if new_mouse_world_pos is None or self.start_mouse_world_pos is None:
            return

        # Create the translation vector
        trans_vec = None
        plane_diff = new_mouse_world_pos - self.start_mouse_world_pos
        if self.direction == TranslateArrowGizmo.DIR_X:
            trans_vec = np.array([plane_diff[0], 0, 0])
        elif self.direction == TranslateArrowGizmo.DIR_Y:
            trans_vec = np.array([0, plane_diff[1], 0])
        else:
            trans_vec = np.array([0, 0, plane_diff[2]])
        if self.translate_callback is not None:
            self.translate_callback(self.component, self.start_pos + trans_vec)

    def handle_drag_stop(self):
        self.get_geom().setColor(self.color)
        if self.translate_finished_callback is not None:
            self.translate_finished_callback(self.component)

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
