"""
Controls the camera.

@author Ben Giacalone
"""

from direct.showbase import DirectObject
from direct.task import Task
from panda3d.core import LVector3f, OrthographicLens
import math


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
        self.delta_mouse = (0, 0)
        self.last_mouse = (0, 0)

        # Register events
        self.accept("mouse2", self.handle_scroll_pressed)
        self.accept("mouse2-up", self.handle_scroll_released)
        self.accept("wheel_up", self.handle_scroll_up)
        self.accept("wheel_down", self.handle_scroll_down)
        self.accept("lshift", self.handle_shift_pressed)
        self.accept("lshift-up", self.handle_shift_released)

        # Set up camera
        self.cam_node.setPos(0, -1, 0)
        self.forward = (-self.cam_node.getPos()).normalized()
        self.up_angle = 0
        self.left_angle = 0
        self.addTask(self.cam_ctrl_task)

    # Scroll wheel button pressed handler
    def handle_scroll_pressed(self):
        self.scroll_down = True

    # Scroll wheel button released handler
    def handle_scroll_released(self):
        self.scroll_down = False

    # Scroll wheel up handler
    def handle_scroll_up(self):
        delta_pos = self.forward * self.ZOOM_LEN
        if (self.cam_node.getPos() + delta_pos).length() >= self.ZOOM_LEN:
            self.cam_node.setPos(self.cam_node.getPos() + delta_pos)

    # Scroll wheel down handler
    def handle_scroll_down(self):
        delta_pos = self.forward * -self.ZOOM_LEN
        if (self.cam_node.getPos() + delta_pos).length() >= self.ZOOM_LEN:
            self.cam_node.setPos(self.cam_node.getPos() + delta_pos)

    # Shift button pressed handler
    def handle_shift_pressed(self):
        self.shift_down = True

    # Shift button released handler
    def handle_shift_released(self):
        self.shift_down = False

    # Camera control task
    def cam_ctrl_task(self, task):
        # Update delta mouse
        curr_mouse = self.last_mouse
        if self.base.mouseWatcherNode.hasMouse():
            curr_mouse = (self.base.mouseWatcherNode.getMouseX(), self.base.mouseWatcherNode.getMouseY())
        delta_mouse = (curr_mouse[0] - self.last_mouse[0], curr_mouse[1] - self.last_mouse[1])
        self.last_mouse = curr_mouse

        if self.scroll_down:
            # Translate if shift is down
            if self.shift_down:
                # TODO: Implement this
                pass
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
        cam_dist = self.cam_node.getPos().length()
        new_x = math.sin(self.up_angle) * math.cos(self.left_angle)
        new_y = math.sin(self.up_angle) * math.sin(self.left_angle)
        new_z = math.cos(self.up_angle)
        new_pos = LVector3f(new_x, new_y, new_z) * cam_dist
        self.cam_node.setPos(new_pos)
        self.forward = (-self.cam_node.getPos()).normalized()
        self.cam_node.lookAt(0, 0, 0)

    # "Destructor" for camera controller
    def destroy(self):
        self.ignore_all()
