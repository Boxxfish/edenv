"""
A list item that can expand to display its children.
Useful for displaying hierarchies.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_list_item import GUIListItem
from tools.envedit.gui.gui_stack_layout import GUIStackLayout


class GUIListDropdown(GUIListItem):

    def __init__(self, text=""):
        GUIListItem.__init__(self)
        self.fit_width_to_content = False
        self.fit_height_to_content = True
        self.expanded = False
        self.sub_list = []
        self.parent = None
        self.level = 0

        self.level_spacer = GUIComponent()
        self.level_spacer.bbox.width = 0
        self.level_spacer.receive_events = False

        self.dropdown_button = GUIButton()
        self.dropdown_button.set_bg_image("right_arrow.png")
        self.dropdown_button.set_bg_color((1, 1, 1, 0.8))
        self.dropdown_button.bbox.width = 16
        self.dropdown_button.on_click = self.on_dropdown_click

        self.spacer = GUIComponent()
        self.spacer.bbox.width = 6
        self.spacer.receive_events = False

        self.label = GUILabel()
        self.label.text_size = 15
        self.label.set_text(text)
        self.label.receive_events = False

        self.layout = GUIStackLayout(vertical=False)
        self.layout.padding = 12
        self.layout.bbox.height = 40
        self.layout.add_child(self.level_spacer)
        self.layout.add_child(self.dropdown_button)
        self.layout.add_child(self.spacer)
        self.layout.add_child(self.label)

        self.set_child(self.layout)

    # Handles the dropdown button being clicked
    def on_dropdown_click(self):
        if self.expanded:
            self.collapse()
        else:
            self.expand()

    # Adds a sub-list item to the dropdown
    def add_sub_item(self, item):
        item.parent = self
        item.level = self.level + 1
        item.level_spacer.bbox.width = 22 * item.level
        self.sub_list.append(item)
        self.update()

    # Expands this dropdown
    def expand(self):
        self.expanded = True
        self.dropdown_button.set_bg_image("down_arrow.png")
        self.list_container.add_sub_list(self)

    # Collapses this dropdown
    def collapse(self):
        self.expanded = False
        self.dropdown_button.set_bg_image("right_arrow.png")
        self.list_container.remove_sub_list(self)
        if self.list_container.selected_item in self.sub_list:
            self.select()

