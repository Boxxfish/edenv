"""
Bounding box for GUI components.

@author Ben Giacalone
"""

class BoundingBox:

    # x and y are the coordinates of the box's left-up corner
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Checks if a point is inside the bounding box
    def point_inside(self, x, y):
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    # Returns a deep copy
    def copy(self):
        return BoundingBox(self.x, self.y, self.width, self.height)
