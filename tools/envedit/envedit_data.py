"""
Data for envedit. The model of MVC.

@author Ben Giacalone
"""
import json

from tools.envedit.edenv_component import EComponent
from tools.envedit.graph_node import GraphNode


class EnveditData:
    TRANSLATE_GIZMO = 0
    ROTATE_GIZMO = 1
    SCALE_GIZMO = 2

    envedit_data = None

    def __init__(self):
        self.scene_root = GraphNode("Scene Root")
        self.target_node = None
        self.dirty = True                          # if the data was changed since saving
        self.save_path = None
        self.project_name = None
        self.update_callback = None
        self.panda_root_node = None
        self.selected_gizmo = EnveditData.TRANSLATE_GIZMO
        EnveditData.envedit_data = self

    # Updates the GUI after any change
    def update(self):
        if self.update_callback is not None:
            self.update_callback()

    # Turns the dirty flag on
    def modify(self):
        self.dirty = True

    # Saves the data
    def save(self, path=None):
        if path is not None:
            self.save_path = path

        with open(self.save_path, "w") as file:
            json.dump(GraphNode.scene_graph_to_dict(self.scene_root), file)

        self.dirty = False
        self.update()

    # Loads the data
    def load(self, path):
        self.save_path = path

        with open(self.save_path, "r") as file:
            file_json = json.load(file)
            self.scene_root = GraphNode.dict_to_scene_graph(file_json)

        self.init_node_components(self.scene_root)

        self.dirty = False
        self.update()

    # Recursive function to update all components after graph is loaded
    def init_node_components(self, node):
        for child in node.children:
            self.init_node_components(child)

        node.component_property_changed()

    # Sets the target node
    def set_target_node(self, node):
        # Call property changed on previous node
        if self.target_node is not None:
            self.target_node.component_property_changed()

        # Call property changed on current node
        self.target_node = node
        if self.target_node is not None:
            self.target_node.component_property_changed_selected()

        self.update()

    # Changes the selected transform gizmo
    def set_transform_gizmo(self, transform_gizmo):
        self.selected_gizmo = transform_gizmo
        if self.target_node is not None:
            self.target_node.component_property_changed_selected()
        self.update()
