"""
A dropdown menu that provides a host of options on click.

@author Ben Giacalone
"""
from enum import Enum, auto

from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_context_menu import GUIContextMenu
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_system import GUISystem


class GUIDropdownVisualType(Enum):
    LABEL = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()


class GUIDropdown(GUIButton):

    def __init__(self, visual=GUIDropdownVisualType.LABEL):
        GUIButton.__init__(self)
        self.bbox.height = 24
        self.padding = 2
        self.set_normal_color((0.1, 0.1, 0.1, 0))
        self.set_hover_color((1, 1, 1, 0.2))
        self.set_pressed_color((0.5, 0.5, 0.5, 1))

        if visual == GUIDropdownVisualType.LABEL:
            self.set_child(GUILabel())
        elif visual == GUIDropdownVisualType.VERTICAL:
            self.fit_width_to_content = True
            self.fit_height_to_content = True
            self.set_child(GUIFrame())
            self.child.bbox.width = 24
            self.child.bbox.height = 24
            self.child.set_bg_color((1, 1, 1, 0.9))
            self.child.set_bg_image("vertical_more.png")
            print(self.child.bbox.width)
        elif visual == GUIDropdownVisualType.HORIZONTAL:
            self.fit_width_to_content = True
            self.fit_height_to_content = True
            self.set_child(GUIFrame())
            self.child.bbox.width = 24
            self.child.bbox.height = 24
            self.child.set_bg_color((1, 1, 1, 0.9))
            self.child.set_bg_image("horizontal_more.png")
        self.child.receive_events = False

        self.menu = GUIContextMenu()

    def handle_left_pressed(self):
        GUIButton.handle_left_pressed(self)
        GUISystem.place_dropdown(self, self.menu)
