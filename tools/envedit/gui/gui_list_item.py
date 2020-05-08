"""
Represents an item in a GUIList.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel


class GUIListItem(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.list_container = None
        self.normal_color = (0.1, 0.1, 0.1, 0)
        self.active_color = (0.5, 0.5, 0.5, 1)
        self.set_bg_color(self.normal_color)

    def handle_left_pressed(self):
        self.select()

    # Selects this item
    def select(self):
        self.set_bg_color(self.active_color)
        self.list_container.set_selected_item(self)

    # Deselects this item
    def deselect(self):
        self.set_bg_color(self.normal_color)

