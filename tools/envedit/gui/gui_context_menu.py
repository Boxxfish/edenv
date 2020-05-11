"""
A context menu that usually gets created on right click.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_stack_layout import GUIStackLayout


class GUIContextMenu(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.bbox.width = 200
        self.fit_height_to_content = True
        self.bg_color = (0.5, 0.5, 0.5, 1)
        self.padding = 1
        self.set_child(GUIStackLayout())
