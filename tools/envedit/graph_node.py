"""
Represents a graph node for EDEnv's internal scene graph representation.

@author Ben Giacalone
"""
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
        node.parent = None
        node.transform.set_parent_matrix(np.identity(4))
        self.children.remove(node)

    # Adds a component to the node
    def add_component(self, component):
        component.node = self
        self.data.append(component)
        component.property_changed()

    # Removes a component from the node
    def remove_component(self, component):
        component.node = None
        self.data.remove(component)
        component.component_removed(component.property_vals)

    # Removes all children from this node.
    def clear(self):
        for _ in range(len(self.children)):
            self.remove_child(self.children[0])

    # Triggers "property_changed" on all attached components
    def component_property_changed(self):
        for component in self.data:
            component.property_changed()

    # Finds a child node in the graph
    def find_child(self, node):
        if self is node:
            return self
        for child in self.children:
            result = child.find_child(node)
            if child is not None:
                return child

    # Finds a child node in the graph by name
    def find_child_by_name(self, name):
        if self.name is name:
            return self
        for child in self.children:
            result = child.find_child(name)
            if child is not None:
                return child

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
        curr_dict["components"] = [component.to_dict() for component in node.data]
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
        for component_dict in node_dict["components"]:
            component = EComponent()
            component.load_from_dict(component_dict)
            node.add_component(component)

        for child in node_dict["children"]:
            node.add_child(GraphNode.dict_to_scene_graph(child))

        return node
