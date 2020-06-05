"""
Utilities to map EDEnv's GUI system to Panda3d's.

@author Ben Giacalone
"""


class GUIUtils:
    window_width = 0
    window_height = 0
    square_size = 0

    # Transforms an EDEnv bbox Panda3d bbox
    @staticmethod
    def get_panda_coords(x, y, width, height):
        # Calculate inner square size and edge offset
        edge_offset = None
        if GUIUtils.window_height > GUIUtils.window_width:
            GUIUtils.square_size = GUIUtils.window_width
            edge_offset = (GUIUtils.window_height - GUIUtils.square_size) / 2
        else:
            GUIUtils.square_size = GUIUtils.window_height
            edge_offset = (GUIUtils.window_width - GUIUtils.square_size) / 2

        # Calculate Panda3d bounding box
        new_width = 2 * width / GUIUtils.square_size
        new_height = 2 * height / GUIUtils.square_size
        new_x = -GUIUtils.window_width / GUIUtils.square_size + 0.5 * new_width + 2 * x / GUIUtils.square_size
        new_y = GUIUtils.window_height / GUIUtils.square_size - 0.5 * new_height - 2 * y / GUIUtils.square_size

        return new_x, new_y, new_width, new_height

    # Transforms an EDEnv bbox Panda3d clipping bbox
    @staticmethod
    def get_panda_clip_coords(x, y, width, height):
        # Calculate Panda3d bounding box
        new_width = width / GUIUtils.window_width
        new_height = height / GUIUtils.window_height
        new_x = x / GUIUtils.window_width
        new_y = 1 - y / GUIUtils.window_height

        return new_x, new_y, new_width, new_height

    # Transforms an EDEnv bbox into a Panda3d text bbox
    @staticmethod
    def get_panda_text_coords(x, y, width, height):
        new_x, new_y, new_width, new_height = GUIUtils.get_panda_coords(x - width / 2, y + height / 2, width, height)
        return new_x, new_y, new_width, new_height

    # Converts Panda3d size into screen space size
    @staticmethod
    def get_screen_space_size(width, height):
        new_width = GUIUtils.square_size * width / 2
        new_height = GUIUtils.square_size * height / 2
        return new_width, new_height
