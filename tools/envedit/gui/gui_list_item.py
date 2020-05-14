"""
Represents an item in a GUIList.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_system import GUISystem


class GUIListItem(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.list_container = None
        self.normal_color = (0.1, 0.1, 0.1, 0)
        self.hover_color = (1, 1, 1, 0.2)
        self.active_color = (0.5, 0.5, 0.5, 1)
        self.set_bg_color(self.normal_color)
        self.select_callback = None         # called when item is selected, with the selected item as a param
        self.right_click_callback = None    # called when item is right clicked
        self.right_release_callback = None    # called when item is right released
        self.data = None                    # can be used to associate GUI with objects, does nothing by itself

    def handle_left_pressed(self):
        self.select()

    def handle_cursor_enter(self):
        if self.list_container.selected_item is not self:
            self.set_bg_color(self.hover_color)

    def handle_cursor_exit(self):
        if self.list_container.selected_item is not self:
            self.set_bg_color(self.normal_color)

    def handle_right_pressed(self):
        self.select()
        if self.right_click_callback is not None:
            self.right_click_callback(self)

    def handle_right_released(self):
        if self.right_release_callback is not None:
            self.right_release_callback(self)

    # Selects this item
    def select(self):
        self.set_bg_color(self.active_color)
        self.list_container.set_selected_item(self)
        if self.select_callback is not None:
            self.select_callback(self)
        GUISystem.set_focus(self)

    # Deselects this item
    def deselect(self):
        self.set_bg_color(self.normal_color)

