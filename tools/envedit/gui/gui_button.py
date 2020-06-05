"""
A button that triggers a callback when clicked.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_system import GUISystem


class GUIButton(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.on_click = None
        self.on_release = None
        self.normal_color = (0, 0, 0, 0.4)
        self.pressed_color = (0, 0, 0, 1)
        self.hover_color = (1, 1, 1, 0.4)
        self.set_bg_color(self.normal_color)
        self.data = None

    def set_normal_color(self, normal_color):
        self.normal_color = normal_color
        self.bg_color = self.normal_color
        self.update(self.bbox)

    def set_pressed_color(self, pressed_color):
        self.pressed_color = pressed_color
        self.update(self.bbox)

    def set_hover_color(self, hover_color):
        self.hover_color = hover_color
        self.update(self.bbox)

    def handle_left_pressed(self):
        self.set_bg_color(self.pressed_color)
        if self.on_click is not None:
            self.on_click(self)
        GUISystem.set_focus(self)

    def handle_left_released(self):
        self.set_bg_color(self.hover_color)
        if self.on_release is not None:
            self.on_release(self)

    def handle_cursor_enter(self):
        self.set_bg_color(self.hover_color)

    def handle_cursor_exit(self):
        self.set_bg_color(self.normal_color)