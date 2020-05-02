"""
Controls the camera.

@author Ben Giacalone
"""

from direct.showbase import DirectObject
from direct.task import Task
from panda3d.core import LVector3f
import math


class CameraController(DirectObject.DirectObject):
    # The amount to zoom in when scrolling
    ZOOM_LEN = 3
    # The amount to rotate when rotating
    ROT_AMOUNT = 1

    def __init__(self, base, cam_node):
        # State vars
        self.scroll_down = False
        self.shift_down = False
        self.cam_node = cam_node
        self.base = base
        self.delta_mouse = (0, 0)
        self.last_mouse = (0, 0)

        # Register events
        self.accept("mouse2", self.handle_scroll_pressed)
        self.accept("mouse2-up", self.handle_scroll_released)
        self.accept("wheel_up", self.handle_scroll_up)
        self.accept("wheel_down", self.handle_scroll_down)
        self.accept("lshift", self.handle_shift_pressed)
        self.accept("lshift-up", self.handle_shift_released)

        # Add camera control task
        self.cam_node.setPos(0, -1, 0)
        self.forward = -self.cam_node.getPos()
        self.up = LVector3f(0, 0, 1)
        self.left = self.forward.cross(self.up)
        self.addTask(self.cam_ctrl_task)

    # Scroll wheel button pressed handler
    def handle_scroll_pressed(self):
        self.scroll_down = True

    # Scroll wheel button released handler
    def handle_scroll_released(self):
        self.scroll_down = False

    # Scroll wheel up handler
    def handle_scroll_up(self):
        facing = self.forward
        delta_pos = facing * self.ZOOM_LEN
        if (self.cam_node.getPos() + delta_pos).length() >= self.ZOOM_LEN:
            self.cam_node.setPos(self.cam_node, delta_pos)

    # Scroll wheel down handler
    def handle_scroll_down(self):
        facing = self.forward
        delta_pos = facing * -self.ZOOM_LEN
        if (self.cam_node.getPos() + delta_pos).length() >= self.ZOOM_LEN:
            self.cam_node.setPos(self.cam_node, delta_pos)

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
                pass
            # Otherwise, just rotate
            else:
                cam_dist = self.cam_node.getPos().length()
                l_delta = -delta_mouse[0] * cam_dist
                f_delta = cam_dist - math.sqrt(cam_dist * cam_dist - l_delta * l_delta)
                delta_vec = self.left * l_delta + self.forward * f_delta
                self.cam_node.setPos(self.cam_node, delta_vec)

                # Update camera vectors
                self.forward = (-self.cam_node.getPos()).normalized()
                self.cam_node.lookAt((0, 0, 0))
                self.left = self.forward.cross(self.up)
        return Task.cont

    # "Destructor" for camera controller
    def destroy(self):
        self.ignore_all()
