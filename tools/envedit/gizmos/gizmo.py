"""
Base class for gizmos.

@author Ben Giacalone
"""

class Gizmo:

    def __init__(self):
        self.object_id = 0

    # Handles the left mouse button being pressed over this gizmo
    def handle_left_pressed(self):
        pass

    # Handles the left mouse button being released over this gizmo
    def handle_left_released(self):
        pass

    # Handles the right mouse button being pressed over this gizmo
    def handle_right_pressed(self):
        pass

    # Handles the right mouse button being released over this gizmo
    def handle_right_released(self):
        pass

    # Handles the cursor entering this gizmo
    def handle_cursor_enter(self):
        pass

    # Handles the cursor exiting this gizmo
    def handle_cursor_exit(self):
        pass

    # Handles the cursor dragging
    def handle_drag(self):
        pass

    # Handles the cursor drag stopping
    def handle_drag_stop(self):
        pass

    # Handles the gizmo losing focus
    def handle_lost_focus(self):
        pass

    # Returns the object ID
    def get_object_id(self):
        return self.object_id

    # Sets the object ID
    def set_object_id(self, object_id):
        self.object_id = object_id

    # Destroys the gizmo
    def destroy(self):
        pass