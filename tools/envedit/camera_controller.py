"""
Controls the camera.

@author Ben Giacalone
"""
from os import path
from pathlib import Path

import numpy as np
from direct.showbase import DirectObject
from direct.task import Task
from panda3d.core import LVector3f, OrthographicLens, NodePath, ShaderAttrib, Shader, Filename
import math

from tools.envedit import helper


class CameraController(DirectObject.DirectObject):
    # The amount to zoom in when scrolling
    ZOOM_LEN = 3
    # The amount to rotate when rotating
    ROT_AMOUNT = 1

    def __init__(self, base, render, cam_node):
        # State vars
        self.scroll_down = False
        self.shift_down = False
        self.cam_node = cam_node
        self.base = base
        self.render = render
        self.cam_active = True
        self.delta_mouse = (0, 0)
        self.last_mouse = (0, 0)
        self.start_mouse = (0, 0)

        self.orbit_center = LVector3f(0, 0, 0)
        self.start_orbit = self.orbit_center
        self.plane_normal = np.array([0, 0, 0])

        # Load skinned shader
        self.base.cam.node().setTagStateKey("shader type")

        shader_folder_path = Path(path.realpath(__file__)).parent.parent.parent / "res/shaders"
        self.skinned_shader = Shader.load(Shader.SL_GLSL,
                                          vertex=Filename(shader_folder_path / "skinned.vert").cStr(),
                                          fragment=Filename(shader_folder_path / "skinned.frag").cStr())

        skinned_render_state = NodePath("")
        skinned_render_state.set_shader(self.skinned_shader)
        self.base.cam.node().setTagState("skinned", skinned_render_state.get_state())

        # Load gizmo shader
        self.gizmo_shader = Shader.load(Shader.SL_GLSL,
                                        vertex=Filename(shader_folder_path / "gizmo.vert").cStr(),
                                        fragment=Filename(shader_folder_path / "gizmo.frag").cStr())

        gizmo_render_state = NodePath("")
        gizmo_render_state.set_shader(self.gizmo_shader)
        self.base.render.set_shader_input("cam_pos", self.cam_node.getPos())
        self.base.cam.node().setTagState("gizmo", gizmo_render_state.get_state())

        # Register events
        self.accept("mouse2", self.handle_scroll_pressed)
        self.accept("mouse2-up", self.handle_scroll_released)
        self.accept("shift-mouse2", self.handle_shift_scroll_pressed)
        self.accept("shift-mouse2-up", self.handle_shift_scroll_released)
        self.accept("wheel_up", self.handle_scroll_up)
        self.accept("wheel_down", self.handle_scroll_down)

        # Set up camera
        self.cam_node.setPos(0, -1, 0)
        self.forward = (-self.cam_node.getPos()).normalized()
        self.up_angle = 0
        self.left_angle = 0
        self.addTask(self.cam_ctrl_task)

    # Scroll wheel button pressed handler
    def handle_scroll_pressed(self):
        if self.cam_active:
            self.scroll_down = True

    # Scroll wheel button released handler
    def handle_scroll_released(self):
        self.scroll_down = False
        self.shift_down = False

    # Scroll wheel button shift pressed handler
    def handle_shift_scroll_pressed(self):
        if self.cam_active:
            self.start_orbit = self.orbit_center
            self.plane_normal = -self.forward
            if self.base.mouseWatcherNode.hasMouse():
                self.start_mouse = (self.base.mouseWatcherNode.getMouseX(), self.base.mouseWatcherNode.getMouseY())
            self.scroll_down = True
            self.shift_down = True

    # Scroll wheel button shift released handler
    def handle_shift_scroll_released(self):
        self.scroll_down = False
        self.shift_down = False

    # Scroll wheel up handler
    def handle_scroll_up(self):
        if self.cam_active:
            delta_pos = self.forward * self.ZOOM_LEN
            if (self.cam_node.getPos() + delta_pos).length() >= self.ZOOM_LEN:
                self.cam_node.setPos(self.cam_node.getPos() + delta_pos)

                # Update camera position in shader
                self.base.render.set_shader_input("cam_pos", self.cam_node.getPos())

    # Scroll wheel down handler
    def handle_scroll_down(self):
        if self.cam_active:
            delta_pos = self.forward * -self.ZOOM_LEN
            if (self.cam_node.getPos() + delta_pos).length() >= self.ZOOM_LEN:
                self.cam_node.setPos(self.cam_node.getPos() + delta_pos)

                # Update camera position in shader
                self.base.render.set_shader_input("cam_pos", self.cam_node.getPos())

    # Camera control task
    def cam_ctrl_task(self, task):
        # Update delta mouse
        curr_mouse = self.last_mouse
        if self.base.mouseWatcherNode.hasMouse():
            curr_mouse = (self.base.mouseWatcherNode.getMouseX(), self.base.mouseWatcherNode.getMouseY())
        delta_mouse = (curr_mouse[0] - self.last_mouse[0], curr_mouse[1] - self.last_mouse[1])
        self.last_mouse = curr_mouse

        if self.scroll_down:
            # Translate camera if shift is down
            if self.shift_down:
                start_point = self.get_ray_plane_intersection(self.start_mouse, np.array([0, 0, 0]),self.plane_normal)
                plane_point = self.get_ray_plane_intersection(curr_mouse, np.array([0, 0, 0]), self.plane_normal)
                self.orbit_center = self.start_orbit - helper.np_vec3_to_panda(plane_point - start_point)

                # Recalculate camera position and direction
                self.update_cam()
            # Otherwise, just rotate
            else:
                # Adjust angles
                self.left_angle += -delta_mouse[0]
                self.up_angle += -delta_mouse[1]

                if self.left_angle > math.pi * 2:
                    self.left_angle -= math.pi * 2
                elif self.left_angle < 0:
                    self.left_angle += math.pi * 2

                if self.up_angle > math.pi * 2:
                    self.up_angle -= math.pi * 2
                elif self.up_angle < 0:
                    self.up_angle += math.pi * 2

                # Recalculate camera position and direction
                self.update_cam()

        return Task.cont

    # Recalculates camera position and direction from spherical coords
    def update_cam(self):
        cam_dist = (self.orbit_center - self.cam_node.getPos()).length()
        new_x = math.sin(self.up_angle) * math.cos(self.left_angle)
        new_y = math.sin(self.up_angle) * math.sin(self.left_angle)
        new_z = math.cos(self.up_angle)
        new_pos = self.orbit_center + LVector3f(new_x, new_y, new_z) * cam_dist
        self.cam_node.setPos(new_pos)
        self.forward = (self.orbit_center - self.cam_node.getPos()).normalized()
        self.cam_node.lookAt(self.orbit_center)

        # Update camera position in shader
        self.base.render.set_shader_input("cam_pos", new_pos)

    # "Destructor" for camera controller
    def destroy(self):
        self.ignore_all()
        self.removeAllTasks()

    # Returns the world space coordinate of a view space point
    # The world space coordinate is projected onto a 2D plane facing the camera
    def view_to_world(self, view_point):
        camera = self.base.camera
        proj_mat = helper.panda_mat4_to_np(self.base.camLens.getProjectionMat())
        cam_mat = np.linalg.inv(helper.panda_mat4_to_np(camera.getTransform().getMat()))
        view_to_world_mat = np.linalg.inv(cam_mat).dot(np.linalg.inv(proj_mat))
        world_point = view_to_world_mat.dot(np.array([view_point[0], view_point[1], -1, 1]))[:3]
        return world_point

    # Returns the world space intersection of a camera ray and a plane
    # The ray is generated from a view space coordinate
    # The plane is in world space
    def get_ray_plane_intersection(self, view_point, plane_center, plane_normal):
        # Convert screen point to ray in world space
        cam_pos = self.base.camera.getTransform().getPos()
        ray_origin = np.array([cam_pos[0], cam_pos[1], cam_pos[2]])
        ray_dir = self.view_to_world(view_point) - ray_origin

        # Calculate intersection
        denom = ray_dir.dot(plane_normal)
        if abs(denom) < 0.001:
            return None
        else:
            multiplier = (plane_center - ray_origin).dot(plane_normal) / denom
            return ray_origin + ray_dir * multiplier
