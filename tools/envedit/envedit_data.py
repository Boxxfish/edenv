"""
Data for envedit. The model of MVC.

@author Ben Giacalone
"""
import json

from tools.envedit.edenv_component import EComponent
from tools.envedit.graph_node import GraphNode


class EnveditData:
    envedit_data = None

    def __init__(self):
        self.scene_root = GraphNode("Scene Root")
        self.target_node = None
        self.dirty = True                          # if the data was changed since saving
        self.save_path = None
        self.project_name = None
        self.update_callback = None
        self.panda_root_node = None
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

        self.dirty = False
        self.update()

    # Sets the target node
    def set_target_node(self, node):
        if self.target_node is not None:
            self.target_node.component_property_changed()
        self.target_node = node
        if self.target_node is not None:
            self.target_node.component_property_changed_selected()
        self.update()
