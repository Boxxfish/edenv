"""
Represents a graph node for EDEnv's internal scene graph representation.

@author Ben Giacalone
"""


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
