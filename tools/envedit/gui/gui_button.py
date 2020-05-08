"""
A button that triggers a callback when clicked.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_frame import GUIFrame


class GUIButton(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.on_click = None

    def handle_left_pressed(self):
        if self.on_click is not None:
            self.on_click()
