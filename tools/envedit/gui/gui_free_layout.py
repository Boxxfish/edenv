"""
GUI layout that allows free positioning of children.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_layout import GUILayout


class GUIFreeLayout(GUILayout):

    def __init__(self):
        GUILayout.__init__(self)
        self.children = []

    # Adds a child to the layout
    def add_child(self, child):
        self.children.append(child)
        self.update()

    def update(self):
        for child in self.children:
            child.update()
