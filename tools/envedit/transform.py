"""
Represents a transform matrix.

@author Ben Giacalone
"""
import numpy as np
from math import cos, sin


class Transform:

    def __init__(self):
        self.matrix = np.identity(4)
        self.dirty = False
        self.trans = np.array([0, 0, 0])
        self.rot = np.array([0, 0, 0])
        self.scale = np.array([1, 1, 1])

    def set_matrix(self, matrix):
        self.matrix = matrix

    def set_translation(self, translation):
        self.trans = translation
        self.dirty = True

    def set_rotation(self, rotation):
        self.rot = rotation
        self.dirty = True

    def set_scale(self, scale):
        self.scale = scale
        self.dirty = True

    def recalculate(self):
        # Obtain scale matrix
        scale_mat = np.array([[self.scale[0], 0, 0, 0],
                              [0, self.scale[1], 0, 0],
                              [0, 0, self.scale[2], 0],
                              [0, 0, 0, 1]])

        # Obtain rotation matrix
        x_rot_mat = np.array([[1, 0, 0, 0],
                              [0, cos(self.rot[0]), -sin(self.rot[0]), 0],
                              [0, 0, sin(self.rot[0]), 0],
                              [0, 0, 0, 1]])
        y_rot_mat = np.array([[cos(self.rot[1]), 0, sin(self.rot[1]), 0],
                              [0, 1, 0, 0],
                              [-sin(self.rot[1]), 0, cos(self.rot[1]), 0],
                              [0, 0, 0, 1]])
        z_rot_mat = np.array([[cos(self.rot[2]), -sin(self.rot[2]), 0, 0],
                              [sin(self.rot[2]), cos(self.rot[2]), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
        rot_mat = z_rot_mat * y_rot_mat * x_rot_mat

        # Obtain translation matrix
        trans_mat = np.array([[1, 0, 0, self.trans[0]],
                           [0, 1, 0, self.trans[1]],
                           [0, 0, 1, self.trans[2]],
                           [0, 0, 0, 1]])

        # Get new matrix by applying scale, rotation, translation
        self.matrix = trans_mat * rot_mat * scale_mat

    # Returns the matrix of the transform
    def get_mat(self):
        if self.dirty:
            self.recalculate()
        return self.matrix
