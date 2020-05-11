"""
Controls the scene graph viewer.

@author Ben Giacalone
"""

from pathlib import Path
from panda3d.core import Filename
from os import path
from tools.envedit.graph_node import GraphNode
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_list import GUIList
from tools.envedit.gui.gui_list_dropdown import GUIListDropdown
from tools.envedit.gui.gui_menu_item import GUIMenuItem
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_system import GUISystem


class GraphViewer(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)

        # Scene graph
        self.envedit_data = None

        # GUI settings
        self.bg_color = (0, 0, 0, 0.8)
        self.bbox.width = 300
        self.padding = 10

        layout = GUIStackLayout()
        self.set_child(layout)

        title = GUILabel()
        title.text_size = 30
        title.set_font(GUISystem.get_font("default_light"))
        title.set_text("Scene Graph")
        layout.add_child(title)

        spacer = GUIComponent()
        spacer.bbox.height = 20
        layout.add_child(spacer)

        self.scene_list = GUIList()
        layout.add_child(self.scene_list)

    # Adds a node from the scene tree to the graph viewer.
    def setup_scene_tree(self, node, parent):
        # Create list item element
        list_item = GUIListDropdown()
        list_item.label.set_text(node.name)
        list_item.data = node
        list_item.select_callback = self.list_item_clicked
        list_item.right_release_callback = self.list_item_right_released
        if type(parent) == GUIList:
            parent.add_item(list_item)
        else:
            parent.add_sub_item(list_item)

        # Propagate to children
        for child in node.children:
            self.setup_scene_tree(child, list_item)

    # Clears all nodes from viewer
    def clear_viewer(self):
        # Removing the root item removes all items in the list
        if len(self.scene_list.child.children) > 0:
            self.scene_list.remove_item(self.scene_list.child.children[0])

    # Sets the data model
    def set_envedit_data(self, envedit_data):
        self.envedit_data = envedit_data

    # Updates the viewer
    def update_viewer(self):
        if self.envedit_data is not None:
            self.clear_viewer()
            self.setup_scene_tree(self.envedit_data.scene_root, self.scene_list)

    # Called when a list item is clicked
    def list_item_clicked(self, item):
        self.envedit_data.target_node = item.data
        self.envedit_data.update()

    # Called when a list item is right clicked
    def list_item_right_released(self, item):
        # Create context menu
        menu = GUISystem.create_context_menu()

        add_node_button = GUIMenuItem()
        add_node_button.child.set_text("Create Child Node")
        menu.child.add_child(add_node_button)

        del_node_button = GUIMenuItem()
        del_node_button.child.set_text("Delete Node")
        menu.child.add_child(del_node_button)

        # No clue why this works
        menu.update()
        menu.update()
