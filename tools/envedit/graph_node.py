"""
Represents a graph node for EDEnv's internal scene graph representation.

@author Ben Giacalone
"""
import math

import numpy as np

from tools.envedit.edenv_component import EComponent
from tools.envedit.transform import Transform


class GraphNode:

    def __init__(self, name="", data=[]):
        self.transform = Transform()
        self.transform.on_matrix_update = self.on_matrix_update
        self.children = []
        self.parent = None
        self.data = data
        for component in data:
            component.node = self
        self.name = name

    # Adds a child node to this node.
    def add_child(self, node):
        node.parent = self
        node.transform.set_parent_matrix(self.transform.get_world_matrix())
        self.children.append(node)

    # Removes a child from this node.
    def remove_child(self, node):
        # Propegate to children
        for child in node.children:
            node.remove_child(child)

        # Remove all components of the removed node
        for component in node.data:
            component.on_gui_remove()

        # Remove node
        node.parent = None
        node.transform.set_parent_matrix(np.identity(4))
        self.children.remove(node)

    # Adds a component to the node
    def add_component(self, component):
        component.node = self
        self.data.append(component)
        component.on_gui_change()

    # Adds a component to the node at index
    def insert_component(self, component, index):
        component.node = self
        self.data.insert(index, component)
        component.on_gui_change()

    # Removes a component from the node
    def remove_component(self, component):
        component.node = None
        self.data.remove(component)
        component.on_gui_remove()

    # Removes all children from this node.
    def clear(self):
        for _ in range(len(self.children)):
            self.remove_child(self.children[0])

    # Triggers "on_gui_change" on all attached components
    def component_property_changed(self):
        for component in self.data:
            component.on_gui_change()

    # Triggers "on_gui_change_selected" on all attached components
    def component_property_changed_selected(self):
        for component in self.data:
            component.on_gui_change_selected()

    # Triggers "on_gui_update" on all attached components
    def component_gui_update(self):
        for component in self.data:
            component.on_gui_update()

    # Finds a child node in the graph
    def find_child(self, node):
        if self is node:
            return self
        for child in self.children:
            result = child.find_child(node)
            if result is not None:
                return result
        return None

    # Finds a child node in the graph by name
    def find_child_by_name(self, name):
        if self.name == name:
            return self
        for child in self.children:
            result = child.find_child_by_name(name)
            if result is not None:
                return result
        return None

    # Handles a matrix update
    def on_matrix_update(self, matrix):
        for child in self.children:
            child.transform.set_parent_matrix(matrix)
            child.component_property_changed()

    # Processes the scene graph and returns a dict representation
    @staticmethod
    def scene_graph_to_dict(node):
        curr_dict = {}
        curr_dict["name"] = node.name
        curr_dict["components"] = [component.to_dict() for component in node.data if component.to_dict()["script_path"] != "components.position"]
        curr_dict["transform"] = node.transform.to_dict()

        child_list = []
        for child in node.children:
            child_list.append(GraphNode.scene_graph_to_dict(child))

        curr_dict["children"] = child_list
        return curr_dict

    # Processes the file dictionary and returns the corresponding graph node
    @staticmethod
    def dict_to_scene_graph(node_dict):
        node = GraphNode()
        node.name = node_dict["name"]
        node.data = []
        node.transform.load_from_dict(node_dict["transform"])

        pos_component = EComponent.from_script("components.position")
        pos_component.property_vals["pos"][0] = str(int(node.transform.trans[0].item() * 1000) / 1000)
        pos_component.property_vals["pos"][1] = str(int(node.transform.trans[1].item() * 1000) / 1000)
        pos_component.property_vals["pos"][2] = str(int(node.transform.trans[2].item() * 1000) / 1000)
        pos_component.property_vals["rot"][0] = str(math.degrees(int(node.transform.rot[0].item() * 1000) / 1000))
        pos_component.property_vals["rot"][1] = str(math.degrees(int(node.transform.rot[1].item() * 1000) / 1000))
        pos_component.property_vals["rot"][2] = str(math.degrees(int(node.transform.rot[2].item() * 1000) / 1000))
        pos_component.property_vals["scale"][0] = str(int(node.transform.scale[0].item() * 1000) / 1000)
        pos_component.property_vals["scale"][1] = str(int(node.transform.scale[1].item() * 1000) / 1000)
        pos_component.property_vals["scale"][2] = str(int(node.transform.scale[2].item() * 1000) / 1000)
        node.add_component(pos_component)

        for component_dict in node_dict["components"]:
            component = EComponent.load_from_dict(component_dict)
            node.add_component(component)

        for child in node_dict["children"]:
            node.add_child(GraphNode.dict_to_scene_graph(child))

        return node
