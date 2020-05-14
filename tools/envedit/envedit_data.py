"""
Data for envedit. The model of MVC.

@author Ben Giacalone
"""
import json

from tools.envedit.edenv_component import EComponent
from tools.envedit.graph_node import GraphNode


class EnveditData:

    def __init__(self):
        self.scene_root = GraphNode("Scene Root")
        self.target_node = None
        self.dirty = True                          # if the data was changed since saving
        self.save_path = None
        self.project_name = None
        self.update_callback = None

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
            json.dump(self.scene_graph_to_dict(self.scene_root), file)

        self.dirty = False
        self.update()

    # Loads the data
    def load(self, path):
        self.save_path = path

        with open(self.save_path, "r") as file:
            file_json = json.load(file)
            self.scene_root = self.dict_to_scene_graph(file_json)

        self.dirty = False
        self.update()

    # Processes the scene graph and returns a dict representation
    def scene_graph_to_dict(self, node):
        curr_dict = {}
        curr_dict["name"] = node.name
        curr_dict["components"] = [component.to_dict() for component in node.data]

        child_list = []
        for child in node.children:
            child_list.append(self.scene_graph_to_dict(child))

        curr_dict["children"] = child_list
        return curr_dict

    # Processes the file dictionary and returns the corresponding graph node
    def dict_to_scene_graph(self, node_dict):
        node = GraphNode()
        node.name = node_dict["name"]
        node.data = []
        for component_dict in node_dict["components"]:
            component = EComponent()
            component.load_from_dict(component_dict)
            node.data.append(component)

        for child in node_dict["children"]:
            node.add_child(self.dict_to_scene_graph(child))

        return node
