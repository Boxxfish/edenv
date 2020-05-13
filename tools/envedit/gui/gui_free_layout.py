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
        if self.rendering:
            child.add_render()
        self.children.append(child)
        self.update()

    # Removes a child from the layout
    def remove_child(self, child):
        child.stop_render()
        self.children.remove(child)
        self.update()

    # Removes all children from the layout
    def clear(self):
        for _ in range(len(self.children)):
            self.remove_child(self.children[0])

    # Checks if this component contains a point in screen space, then propagates to children
    # Note: this layout cannot respond to events
    def get_selected_component(self, x, y):
        if self.bbox.point_inside(x, y):
            for child in self.children:
                child_component = child.get_selected_component(x, y)
                if child_component is not None:
                    return child_component
        return None

    def update(self):
        for child in self.children:
            # If child is outside bounds, reposition it back in
            if child.bbox.x + child.bbox.width > self.bbox.x + self.bbox.width:
                child.bbox.x -= (child.bbox.x + child.bbox.width) - (self.bbox.x + self.bbox.width)
            if child.bbox.y + child.bbox.height > self.bbox.y + self.bbox.height:
                child.bbox.y -= (child.bbox.y + child.bbox.height) - (self.bbox.y + self.bbox.height)

            child.update()

    def add_render(self):
        self.rendering = True
        if self.rendering:
            for child in self.children:
                child.add_render()

    def stop_render(self):
        self.rendering = False
        for child in self.children:
            child.stop_render()
