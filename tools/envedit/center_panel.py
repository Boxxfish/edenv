"""
Envedit's center panel.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_component import GUIComponent


class CenterPanel(GUIComponent):

    def __init__(self, cam_controller):
        GUIComponent.__init__(self)
        self.cam_controller = cam_controller

    def handle_cursor_enter(self):
        self.cam_controller.cam_active = True

    def handle_cursor_exit(self):
        self.cam_controller.cam_active = False