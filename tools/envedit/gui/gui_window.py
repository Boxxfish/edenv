"""
Represents a window to render GUI components to.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_component import GUIComponent


class GUIWindow(GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)

    # Called when window is resized
    def window_resized(self, width, height):
        self.bbox.width = width
        self.bbox.height = height
        self.update()

    def update(self):
        if self.child is not None:
            self.child.bbox = self.bbox.copy()
            self.child.update()
