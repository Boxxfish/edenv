"""
A dropdown menu that provides a host of options on click.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_context_menu import GUIContextMenu
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_system import GUISystem


class GUIDropdown(GUIButton):

    def __init__(self):
        GUIButton.__init__(self)
        self.bbox.height = 24
        self.padding = 2
        self.set_normal_color((0.1, 0.1, 0.1, 0))
        self.set_hover_color((1, 1, 1, 0.2))
        self.set_pressed_color((0.5, 0.5, 0.5, 1))

        self.child = GUILabel()
        self.child.receive_events = False

        self.menu = GUIContextMenu()

    def handle_left_pressed(self):
        GUIButton.handle_left_pressed(self)
        GUISystem.place_dropdown(self, self.menu)
