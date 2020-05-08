"""
Base class for layout components.
Layouts automatically adjust the position of their children.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_component import GUIComponent


class GUILayout(GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)

    # Override set_child so add_child can be used instead
    def set_child(self, child):
        raise Exception("GUILayout has children, not single child. Use set_child")
