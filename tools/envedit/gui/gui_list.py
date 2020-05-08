"""
Contains a series of list items.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_list_dropdown import GUIListDropdown
from tools.envedit.gui.gui_stack_layout import GUIStackLayout


class GUIList(GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)
        self.child = GUIStackLayout()
        self.selected_item = None

    # Sets the selected item
    def set_selected_item(self, item):
        self.selected_item = item
        for child in self.child.children:
            if child is not item:
                child.deselect()

    # Adds an item to the list
    def add_item(self, item, index=-1):
        item.list_container = self
        self.child.add_child(item, index)
        self.update()

    # Removes an item from the list
    def remove_item(self, item):
        self.child.remove_child(item)
        self.update()

    # Adds the parent's sub-list to the list
    def add_sub_list(self, parent):
        p_index = self.child.children.index(parent)
        for list_item in parent.sub_list:
            self.add_item(list_item, p_index + 1)

    # Removes the parent's sub-list from the list
    def remove_sub_list(self, parent):
        # Find the parent in the list
        for list_item in parent.sub_list:
            self.remove_item(list_item)

    def update(self):
        self.child.bbox.x = self.bbox.x
        self.child.bbox.y = self.bbox.y
        self.child.bbox.width = self.bbox.width
        self.child.update()
        self.bbox.height = self.child.bbox.height
