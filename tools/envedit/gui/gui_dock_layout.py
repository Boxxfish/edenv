"""
GUI layout that docks elements to the side of the container.
The layout prioritizes the top and bottom elements, so they are laid out like this:

      T
-------------
   |     |
L  |  C  | R
   |     |
-------------
      B

@author Ben Giacalone
"""
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_layout import GUILayout


class GUIDockLayout(GUILayout):
    # Enum values for dock
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOTTOM = 3
    CENTER = 4

    def __init__(self):
        GUILayout.__init__(self)
        self.left_child = GUIComponent()
        self.right_child = GUIComponent()
        self.top_child = GUIComponent()
        self.bottom_child = GUIComponent()
        self.center_child = GUIComponent()

    def update(self):
        self.top_child.bbox.x = self.bbox.x
        self.top_child.bbox.y = self.bbox.y
        self.top_child.bbox.width = self.bbox.width
        self.top_child.update()

        self.bottom_child.bbox.x = self.bbox.x
        self.bottom_child.bbox.y = self.bbox.height - self.bottom_child.bbox.height
        self.bottom_child.bbox.width = self.bbox.width
        self.bottom_child.update()

        self.left_child.bbox.x = self.bbox.x
        self.left_child.bbox.y = self.bbox.y + self.top_child.bbox.height
        self.left_child.bbox.height = self.bbox.height - (self.top_child.bbox.height + self.bottom_child.bbox.height)
        self.left_child.update()

        self.right_child.bbox.x = self.bbox.width - self.right_child.bbox.width
        self.right_child.bbox.y = self.bbox.y + self.top_child.bbox.height
        self.right_child.bbox.height = self.bbox.height - (self.top_child.bbox.height + self.bottom_child.bbox.height)
        self.right_child.update()

        self.center_child.bbox.x = self.bbox.x + self.left_child.bbox.width
        self.center_child.bbox.y = self.bbox.y + self.top_child.bbox.height
        self.center_child.bbox.width = self.bbox.width - (self.left_child.bbox.width + self.right_child.bbox.width)
        self.center_child.bbox.height = self.bbox.height - (self.top_child.bbox.height + self.bottom_child.bbox.height)
        self.center_child.update()

    # Sets the docked child
    def set_child_dock(self, child, dock_dir):
        if self.rendering:
            child.add_render()
        if dock_dir == GUIDockLayout.LEFT:
            self.left_child = child
        elif dock_dir == GUIDockLayout.RIGHT:
            self.right_child = child
        elif dock_dir == GUIDockLayout.TOP:
            self.top_child = child
        elif dock_dir == GUIDockLayout.BOTTOM:
            self.bottom_child = child
        elif dock_dir == GUIDockLayout.CENTER:
            self.center_child = child
        self.update()

    # Checks if this component contains a point in screen space, then propagates to children
    def get_selected_component(self, x, y):
        if self.bbox.point_inside(x, y):
            children = [None if self.left_child is None else self.left_child.get_selected_component(x, y),
                        None if self.right_child is None else self.right_child.get_selected_component(x, y),
                        None if self.top_child is None else self.top_child.get_selected_component(x, y),
                        None if self.bottom_child is None else self.bottom_child.get_selected_component(x, y),
                        None if self.center_child is None else self.center_child.get_selected_component(x, y)]
            for child in children:
                if child is not None:
                    return child
            return self
        return None

    def add_render(self):
        self.rendering = True
        children = [self.left_child, self.right_child, self.top_child, self.bottom_child, self.center_child]
        for child in children:
            if child is not None:
                child.add_render()
        self.update()

    def stop_render(self):
        self.rendering = False
        children = [self.left_child, self.right_child, self.top_child, self.bottom_child, self.center_child]
        for child in children:
            if child is not None:
                child.stop_render()
        self.update()
