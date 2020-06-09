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

    # Checks if two bounding boxes intersect
    def intersects(self, other):
        within_x = abs((self.x + self.width / 2) - (other.x + other.width / 2)) < ((self.width + other.width) / 2)
        within_y = abs((self.y + self.height / 2) - (other.y + other.height / 2)) < ((self.height + other.height) / 2)
        return within_x and within_y

    # Returns the intersection of 2 bounding boxes
    def get_intersection(self, other):
        if not self.intersects(other):
            return BoundingBox(0, 0, 0, 0)

        intersection = BoundingBox()
        intersection.x = max(self.x, other.x)
        intersection.y = max(self.y, other.y)
        intersection.width = min(self.x + self.width, other.x + other.width) - intersection.x
        intersection.height = min(self.y + self.height, other.y + other.height) - intersection.y
        return intersection

    # Returns a deep copy
    def copy(self):
        return BoundingBox(self.x, self.y, self.width, self.height)
