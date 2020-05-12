"""
A context menu item.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_system import GUISystem


class GUIMenuItem(GUIButton):

    def __init__(self):
        GUIButton.__init__(self)
        self.child = GUILabel()
        self.child.receive_events = False
        self.bbox.height = 20
        self.set_normal_color((0.2, 0.2, 0.2, 1))
        self.set_hover_color((0.4, 0.4, 0.4, 1))
        self.set_pressed_color((0.4, 0.4, 0.4, 1))
        self.padding = 1

    def handle_left_released(self):
        GUIButton.handle_left_released(self)
        GUISystem.close_context_menu()
