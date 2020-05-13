"""
GUI layout that lays out elements sequentially.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_layout import GUILayout


class GUIStackLayout(GUILayout):

    def __init__(self, vertical=True):
        GUILayout.__init__(self)
        self.children = []
        self.vertical = vertical
        self.padding = 0

    def update(self):
        if self.vertical:
            next_y = 0
            for child in self.children:
                child.bbox.x = self.bbox.x + self.padding
                child.bbox.y = self.bbox.y + self.padding + next_y
                child.bbox.width = self.bbox.width - self.padding * 2
                child.update()
                next_y += child.bbox.height
            self.bbox.height = next_y
        else:
            next_x = 0
            for child in self.children:
                child.bbox.x = self.bbox.x + self.padding + next_x
                child.bbox.y = self.bbox.y + self.padding
                child.bbox.height = self.bbox.height - self.padding * 2
                child.update()
                next_x += child.bbox.width
            self.bbox.width = next_x

    # Adds a child to the layout
    def add_child(self, child, index=-1):
        if index == -1:
            self.children.append(child)
        else:
            self.children.insert(index, child)
        if self.rendering:
            child.add_render()
        self.update()

    # Removes a child from the layout
    def remove_child(self, child):
        child.stop_render()
        if child in self.children:
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

    def add_render(self):
        self.rendering = True
        if self.rendering:
            for child in self.children:
                child.add_render()

    def stop_render(self):
        self.rendering = False
        for child in self.children:
            child.stop_render()
