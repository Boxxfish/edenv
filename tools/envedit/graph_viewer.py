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
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_system import GUISystem


class GraphViewer(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)

        # Scene graph
        self.scene_root = GraphNode(name="Scene Root")
        graph_a = GraphNode(name="Object A")
        graph_a.add_child(GraphNode(name="Object 1"))
        graph_a.add_child(GraphNode(name="Object 2"))
        self.scene_root.add_child(graph_a)
        self.scene_root.add_child(GraphNode(name="Object B"))

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

        scene_list = GUIList()
        layout.add_child(scene_list)

        # Set up scene tree
        self.setup_scene_tree(self.scene_root, scene_list)
        self.update()

    # Adds a node from the scene tree to the graph viewer.
    def setup_scene_tree(self, node, parent):
        # Create list item element
        list_item = GUIListDropdown()
        list_item.label.set_text(node.name)
        if type(parent) == GUIList:
            parent.add_item(list_item)
        else:
            parent.add_sub_item(list_item)

        # Propagate to children
        for child in node.children:
            self.setup_scene_tree(child, list_item)
