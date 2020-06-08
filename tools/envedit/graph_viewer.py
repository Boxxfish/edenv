"""
Controls the scene graph viewer.

@author Ben Giacalone
"""
import json

from tools.envedit.edenv_component import EComponent
from tools.envedit.graph_node import GraphNode
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_list import GUIList
from tools.envedit.gui.gui_list_dropdown import GUIListDropdown
from tools.envedit.gui.gui_menu_item import GUIMenuItem
from tools.envedit.gui.gui_scroll_container import GUIScrollContainer
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_system import GUISystem
from tools.envedit.gui.gui_text_box import GUITextBox
from tkinter import filedialog


class GraphViewer(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)

        # Scene graph
        self.envedit_data = None

        # GUI settings
        self.bg_color = (0, 0, 0, 0.8)
        self.bbox.width = 300
        self.padding = 10

        master_layout = GUIDockLayout()
        self.set_child(master_layout)

        layout = GUIStackLayout()
        master_layout.set_child_dock(layout, GUIDockLayout.TOP)

        title = GUILabel()
        title.text_size = 30
        title.set_font(GUISystem.get_font("default_light"))
        title.set_text("Scene Graph")
        layout.add_child(title)

        spacer = GUIComponent()
        spacer.bbox.height = 20
        layout.add_child(spacer)

        scroll_container = GUIScrollContainer(scroll_v=True, scroll_h=True)
        master_layout.set_child_dock(scroll_container, GUIDockLayout.CENTER)

        self.scene_list = GUIList()
        scroll_container.set_child(self.scene_list)

    # Adds a node from the scene tree to the graph viewer.
    def setup_scene_tree(self, node, parent):
        # Create list item element
        list_item = None
        if type(parent) == GUIList:
            for item in parent.child.children:
                if item.data is node:
                    list_item = item
                    break
        else:
            for item in parent.sub_list:
                if item.data is node:
                    list_item = item
                    break

        # If list item was not found, insert the new item into the hierarchy
        if list_item is None:
            node.pressed_callback = self.node_pressed_handler
            list_item = self.create_new_item(node)

            # For the root node, just add it to the scene list
            if type(parent) == GUIList:
                self.scene_list.child.clear()
                parent.add_item(list_item)

            # Expand the parent if it's a collapsed dropdown, and add to the scene list
            else:
                if not parent.expanded:
                    parent.expand()
                parent.add_sub_item(list_item)
                self.scene_list.add_item(list_item, self.scene_list.child.children.index(parent) + 1)

        # Propagate to children
        for child in node.children:
            self.setup_scene_tree(child, list_item)

        # If there exist any sub items of list_item that aren't children of the node, remove them
        for child in list_item.sub_list:
            if child.data not in node.children:
                list_item.remove_sub_item(child)
                self.scene_list.remove_item(child)

    # Clears all nodes from viewer
    def clear_viewer(self):
        # Removing the root item removes all items in the list
        if len(self.scene_list.child.children) > 0:
            self.scene_list.remove_item(self.scene_list.child.children[0])

    # Creates a new list item based off the scene node
    def create_new_item(self, node):
        list_item = GUIListDropdown()
        list_item.label.set_text(node.name)
        list_item.data = node
        list_item.select_callback = self.list_item_clicked
        list_item.right_release_callback = self.list_item_right_released
        return list_item

    # Sets the data model
    def set_envedit_data(self, envedit_data):
        self.envedit_data = envedit_data
        self.setup_scene_tree(self.envedit_data.scene_root, self.scene_list)

    # Updates the viewer
    def update_viewer(self):
        if self.envedit_data is not None:
            self.setup_scene_tree(self.envedit_data.scene_root, self.scene_list)

            # If target_node is in list, select it
            if self.scene_list.selected_item is None or (self.envedit_data.target_node is not None and self.scene_list.selected_item.data is not self.envedit_data.target_node):
                for list_item in self.scene_list.child.children:
                    if list_item.data is self.envedit_data.target_node:
                        list_item.select()
                        break

            self.update(self.bbox)

    # Called when a list item is clicked
    def list_item_clicked(self, item):
        self.envedit_data.set_target_node(item.data)

    # Called when a list item is right clicked
    def list_item_right_released(self, item):
        # Create context menu
        menu = GUISystem.create_context_menu()

        add_node_button = GUIMenuItem()
        add_node_button.child.set_text("Create Child Node")
        add_node_button.on_release = self.add_node_handler
        add_node_button.data = item
        menu.child.add_child(add_node_button)

        if item.data is not self.envedit_data.scene_root:
            del_node_button = GUIMenuItem()
            del_node_button.child.set_text("Delete Node")
            del_node_button.on_release = self.del_node_handler
            del_node_button.data = item
            menu.child.add_child(del_node_button)

            ren_node_button = GUIMenuItem()
            ren_node_button.child.set_text("Rename Node")
            ren_node_button.on_release = self.ren_node_handler
            ren_node_button.data = item
            menu.child.add_child(ren_node_button)

        export_node_button = GUIMenuItem()
        export_node_button.child.set_text("Export Node Tree")
        export_node_button.on_release = self.export_node_handler
        export_node_button.data = item
        menu.child.add_child(export_node_button)

        # No clue why this works
        menu.update(self.bbox)
        menu.update(self.bbox)

    # Handles a node being selected
    def node_pressed_handler(self, node):
        self.envedit_data.target_node = node
        self.envedit_data.update()

    # Handles the "add node" option being selected
    def add_node_handler(self, item):
        # Create new node
        pos_comp = EComponent.from_script("components.position")
        pos_comp.property_vals["scale"][0] = "1"
        pos_comp.property_vals["scale"][1] = "1"
        pos_comp.property_vals["scale"][2] = "1"
        new_node = GraphNode(f"New Node ({len(item.data.sub_list)})", [pos_comp])
        item.data.data.add_child(new_node)
        new_node.component_property_changed()

        # Update model
        self.envedit_data.modify()
        self.envedit_data.update()

    # Handles the "delete node" option being selected
    def del_node_handler(self, item):
        # Delete node from graph
        item.data.data.parent.remove_child(item.data.data)

        # Update model
        self.envedit_data.modify()
        self.envedit_data.update()

    # Handles the "rename node" option being selected
    def ren_node_handler(self, item):
        # Replace list label with textbox
        node_name = item.data.data.name
        text_box = GUITextBox()
        text_box.data = item.data
        text_box.set_text(node_name)
        item.data.child.remove_child(item.data.child.children[3])
        item.data.child.add_child(text_box)
        text_box.handle_left_pressed()
        text_box.on_lost_focus = self.rename_lost_focus

    # Handles the "export node tree" option being selected
    def export_node_handler(self, item):
        # Open file dialog
        filetypes = [("JSON", "*.json")]
        file_path = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes)

        # Save graph node
        file_dict = GraphNode.scene_graph_to_dict(item.data.data)
        with open(file_path, "w") as file:
            json.dump(file_dict, file)

    # Handles losing focus of renaming text box
    def rename_lost_focus(self, item):
        # Check if name was changed
        if item.data.data.name != item.text:
            self.envedit_data.modify()

        # Replace textbox with list label
        item.data.data.name = item.text
        label = GUILabel()
        label.text_size = 15
        label.receive_events = False
        label.set_text(item.data.data.name)
        item.data.child.remove_child(item.data.child.children[3])
        item.data.child.add_child(label)
