"""
GUI layout that lays out elements in a grid.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_layout import GUILayout


class GUIGridLayout(GUILayout):

    def __init__(self, rows=1, columns=1):
        GUILayout.__init__(self)
        self.rows = rows
        self.columns = columns
        self.children = [[None for _ in range(self.columns)] for _ in range(self.rows)]

    def update(self, parent_bbox):
        cell_width = self.bbox.width / self.columns
        cell_height = self.bbox.height / self.rows
        for r in range(self.rows):
            for c in range(self.columns):
                child = self.children[r][c]
                if child is not None:
                    child.bbox.x = c * cell_width
                    child.bbox.y = r * cell_height
                    child.bbox.width = cell_width
                    child.bbox.height = cell_height
                    child.update(self.bbox)

    # Set cell element at row, column
    def set_child_cell(self, child, row, column):
        if self.rendering:
            child.add_render()
        self.children[row][column] = child
        self.update()

    # Checks if this component contains a point in screen space, then propagates to children
    def get_selected_component(self, x, y):
        if self.bbox.point_inside(x, y):
            for child_col in self.children:
                for child in child_col:
                    child_component = child.get_selected_component(x, y)
                    if child_component is not None:
                        return child_component
            return self
        return None

    def add_render(self):
        self.rendering = True
        for child_col in self.children:
            for child in child_col:
                child.add_render()

    def stop_render(self):
        self.rendering = False
        for child_col in self.children:
            for child in child_col:
                child.stop_render()
