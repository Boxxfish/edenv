"""
Represents a graph node for EDEnv's internal scene graph representation.

@author Ben Giacalone
"""
from tools.envedit.edenv_component import EComponent


class GraphNode():

    def __init__(self, name="", data=None):
        self.children = []
        self.parent = None
        self.data = data
        self.name = name

    # Adds a child node to this node.
    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    # Removes a child from this node.
    def remove_child(self, node):
        node.parent = None
        self.children.remove(node)

    # Removes all children from this node.
    def clear(self):
        for _ in range(len(self.children)):
            self.remove_child(self.children[0])

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

    # Processes the scene graph and returns a dict representation
    @staticmethod
    def scene_graph_to_dict(node):
        curr_dict = {}
        curr_dict["name"] = node.name
        curr_dict["components"] = [component.to_dict() for component in node.data]

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
        for component_dict in node_dict["components"]:
            component = EComponent()
            component.load_from_dict(component_dict)
            node.data.append(component)

        for child in node_dict["children"]:
            node.add_child(GraphNode.dict_to_scene_graph(child))

        return node
