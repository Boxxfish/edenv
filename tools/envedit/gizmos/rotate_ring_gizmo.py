"""
A ring gizmo for rotation.

@author Ben Giacalone
"""
import json
import math
from os import path
from pathlib import Path

import numpy as np

from tools.envedit import helper
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo


class RotateRingGizmo(MeshGizmo):
    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    # axis: the axis the ring is aligned to
    def __init__(self, axis):
        MeshGizmo.__init__(self)
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.start_mouse_world_pos = np.array([0, 0, 0, 1])
        self.rotate_callback = None
        self.rotate_finished_callback = None
        self.component = None
        self.start_pos = np.array([0, 0, 0])
        self.axis = axis

        # Load ring mesh file
        ring_json = None
        ring_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/meshes/rotate_ring.json"
        with open(ring_path, "r") as file:
            ring_json = json.load(file)

        # Generate mesh (renders on top of everything else)
        MeshGizmo.gen_geom(self, ring_json)
        self.get_geom().setColor(self.color)
        self.get_geom().setBin("fixed", 0)
        self.get_geom().setDepthTest(False)
        self.get_geom().setLightOff()

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
        self.start_rot = self.component.node.transform.get_rotation()

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

        # Create the rotation vector
        rot_vec = None
        plane_diff = new_mouse_world_pos - self.start_mouse_world_pos
        if self.axis == RotateRingGizmo.AXIS_X:
            rot_vec = np.array([-plane_diff[1], 0, 0])
        elif self.axis == RotateRingGizmo.AXIS_Y:
            rot_vec = np.array([0, -plane_diff[0], 0])
        else:
            rot_vec = np.array([0, 0, -plane_diff[2]])
        if self.rotate_callback is not None:
            self.rotate_callback(self.component, self.start_rot + rot_vec)

    def handle_drag_stop(self):
        self.get_geom().setColor(self.color)
        if self.rotate_finished_callback is not None:
            self.rotate_finished_callback(self.component)

    # Returns the world space coordinate of a screen space point
    # The world space coordinate is projected onto a 2D plane through the origin facing the camera
    def screen_to_world(self, screen_point):
        camera = GizmoSystem.gizmo_system.base.camera
        dist = (camera.getTransform().getPos() - self.geom_path.getPos()).length()
        screen_mat = np.array([[1 / dist, 0, 0, 0],
                               [0, 1 / dist, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
        proj_mat = helper.panda_mat4_to_np(GizmoSystem.gizmo_system.base.camLens.getProjectionMat())
        view_mat = np.linalg.inv(helper.panda_mat4_to_np(camera.getTransform().getMat()))
        screen_to_world_mat = np.linalg.inv(screen_mat.dot(proj_mat.dot(view_mat)))
        return screen_to_world_mat.dot(screen_point)
