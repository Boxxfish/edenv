"""
A textbox that ensures only numbers are entered.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_text_box import GUITextBox
import string


class GUINumberBox(GUIFrame):

    # use_int: whether the number box should lock to integers or floats
    # step: the amount the number box changes by when an arrow button is pressed
    def __init__(self, use_int=False, step=.1):
        GUIFrame.__init__(self)
        self.use_int = use_int
        self.step = step
        if self.use_int:
            self.step = 1
        self.bbox.height = 20
        self.bbox.width = 100
        self.data = None

        layout = GUIDockLayout()
        self.set_child(layout)

        self.text_box = GUITextBox()
        self.text_box.validate_text = self.validate_text
        layout.set_child_dock(self.text_box, GUIDockLayout.CENTER)

        button_layout = GUIStackLayout()
        button_layout.bbox.width = 20
        layout.set_child_dock(button_layout, GUIDockLayout.RIGHT)

        up_button = GUIButton()
        up_button.bbox.height = 10
        up_button.bbox.width = 20
        up_button.on_click = self.up_arrow_pressed
        up_button.set_bg_image("up_arrow.png")
        button_layout.add_child(up_button)

        down_button = GUIButton()
        down_button.bbox.height = 10
        down_button.bbox.width = 20
        down_button.on_click = self.down_arrow_pressed
        down_button.set_bg_image("down_arrow.png")
        button_layout.add_child(down_button)

    def up_arrow_pressed(self, item):
        if not self.validate_text(self.text_box.text):
            return

        new_val = 0
        if self.use_int:
            new_val = int(self.text_box.text) + self.step
        else:
            new_val = int((float(self.text_box.text) + self.step) * 1000) / 1000
        self.text_box.set_text(str(new_val))

    def down_arrow_pressed(self, item):
        if not self.validate_text(self.text_box.text):
            return

        new_val = 0
        if self.use_int:
            new_val = int(self.text_box.text) - self.step
        else:
            new_val = int((float(self.text_box.text) - self.step) * 1000) / 1000
        self.text_box.set_text(str(new_val))

    def validate_text(self, text):
        if self.use_int:
            return text.lstrip("+-").isdigit()
        else:
            return text.lstrip("+-").replace(".", "", 1).isdigit()
