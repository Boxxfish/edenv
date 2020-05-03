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