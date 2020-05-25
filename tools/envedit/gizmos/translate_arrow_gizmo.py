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

from tools.envedit import helper
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo
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

    # Sets arrow's color
    def set_color(self, color):
        self.color = color
        self.get_geom().setColor(self.color)

    def handle_left_pressed(self):
        # Get starting position of node and projected mouse
        screen_mouse_pos = np.array([GizmoSystem.gizmo_system.raw_mouse_x,
                                     GizmoSystem.gizmo_system.raw_mouse_y,
                                     0,
                                     1])
        self.start_mouse_world_pos = self.screen_to_world(screen_mouse_pos)
        self.start_pos = self.component.node.transform.get_world_translation()

        # Tell gizmo to start dragging
        GizmoSystem.set_drag(self)
        self.get_geom().setColor(self.color[0] - 0.2, self.color[1] - 0.2, self.color[2] - 0.2, self.color[3])

    def handle_left_released(self):
        self.get_geom().setColor(self.color)

    def handle_drag(self):
        # Get projected coordinates of new mouse
        screen_mouse_pos = np.array([GizmoSystem.gizmo_system.raw_mouse_x,
                                     GizmoSystem.gizmo_system.raw_mouse_y,
                                     0,
                                     1])
        new_mouse_world_pos = self.screen_to_world(screen_mouse_pos)

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

    # Returns the world space coordinate of a screen space point
    # The world space coordinate is projected onto a 2D plane through the origin facing the camera
    def screen_to_world(self, screen_point):
        camera = GizmoSystem.gizmo_system.base.camera
        screen_mat = np.array([[1 / camera.getTransform().getPos().length(), 0, 0, 0],
                               [0, 1 / camera.getTransform().getPos().length(), 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
        proj_mat = helper.panda_mat4_to_np(GizmoSystem.gizmo_system.base.camLens.getProjectionMat())
        view_mat = np.linalg.inv(helper.panda_mat4_to_np(camera.getTransform().getMat()))
        screen_to_world_mat = np.linalg.inv(screen_mat.dot(proj_mat.dot(view_mat)))
        return screen_to_world_mat.dot(screen_point)
