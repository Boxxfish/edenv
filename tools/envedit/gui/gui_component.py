"""
Base class for GUI components.

@author Ben Giacalone
"""
from tools.envedit.gui.bounding_box import BoundingBox


class GUIComponent:

    def __init__(self):
        self.bbox = BoundingBox()
        self.child = None
        self.gui_system = None
        self.receive_events = True
        self.rendering = False

    # Sets the child of the component
    def set_child(self, child):
        self.child = child
        if self.rendering:
            self.child.add_render()
        self.update()

    # Updates the component after a change
    def update(self):
        if self.child is not None:
            self.child.update()

    # Removes the element and its child(ren) from the render tree
    def stop_render(self):
        self.rendering = False
        if self.child is not None:
            self.child.stop_render()
        self.update()

    # Adds the element and its child(ren) to the render tree
    def add_render(self):
        self.rendering = True
        if self.child is not None:
            self.child.add_render()
        self.update()

    # Checks if this component contains a point in screen space, then propagates to child
    def get_selected_component(self, x, y):
        if self.bbox.point_inside(x, y) and self.receive_events:
            child_component = None if self.child is None else self.child.get_selected_component(x, y)
            return child_component if child_component is not None else self
        return None

    # Handles the left mouse button being pressed over this component
    def handle_left_pressed(self):
        pass

    # Handles the left mouse button being released over this component
    def handle_left_released(self):
        pass

    # Handles the right mouse button being pressed over this component
    def handle_right_pressed(self):
        pass

    # Handles the right mouse button being released over this component
    def handle_right_released(self):
        pass

    # Handles the cursor entering this component
    def handle_cursor_enter(self):
        pass

    # Handles the cursor exiting this component
    def handle_cursor_exit(self):
        pass

