"""
Data for envedit. The model of MVC.

@author Ben Giacalone
"""
from tools.envedit.graph_node import GraphNode


class EnveditData:

    def __init__(self):
        self.scene_root = GraphNode("Scene Root")
        self.target_node = None
        self.dirty = True                          # if the data was changed since saving
        self.update_callback = None

    # Updates the GUI after any change
    def update(self):
        if self.update_callback is not None:
            self.update_callback()

    # Turns the dirty flag on
    def modify(self):
        self.dirty = True