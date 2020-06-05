"""
Represents a window to render GUI components to.

@author Ben Giacalone
"""
from tools.envedit.gui.bounding_box import BoundingBox
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_free_layout import GUIFreeLayout


class GUIWindow(GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)
        self.context_menu_layer = GUIFreeLayout()
        self.selected_context_menu = False

    # Called when window is resized
    def window_resized(self, width, height):
        self.bbox.width = width
        self.bbox.height = height
        self.update(BoundingBox())

    def update(self, parent_bbox):
        self.context_menu_layer.bbox = self.bbox.copy()
        self.context_menu_layer.update(self.bbox)
        if self.child is not None:
            self.child.bbox = self.bbox.copy()
            self.child.update(self.bbox)

    def get_selected_component(self, x, y):
        if self.bbox.point_inside(x, y) and self.receive_events:
            ctx_component = self.context_menu_layer.get_selected_component(x, y)
            if ctx_component is not None:
                self.selected_context_menu = True
                return ctx_component
            child_component = self.child.get_selected_component(x, y)
            self.selected_context_menu = False
            return self if child_component is None else child_component
        return None

    # Removes the element and its child(ren) from the render tree
    def stop_render(self):
        self.rendering = False
        self.context_menu_layer.stop_render()
        if self.child is not None:
            self.child.stop_render()
        self.update(BoundingBox())

    # Adds the element and its child(ren) to the render tree
    def add_render(self):
        self.rendering = True
        self.context_menu_layer.add_render()
        if self.child is not None:
            self.child.add_render()
        self.update(BoundingBox())
