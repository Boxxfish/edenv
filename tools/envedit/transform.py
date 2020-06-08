"""
Represents a transform matrix.

@author Ben Giacalone
"""
import numpy as np
from math import cos, sin, atan2, sqrt


class Transform:

    def __init__(self):
        self.local_matrix = np.identity(4)
        self.parent_matrix = np.identity(4)
        self.dirty = False
        self.trans = np.array([0, 0, 0])
        self.rot = np.array([0, 0, 0])
        self.scale = np.array([1, 1, 1])
        self.on_matrix_update = None  # Callback is called when transform is changed

    # Sets the parent matrix of the transform
    def set_parent_matrix(self, matrix):
        self.parent_matrix = matrix
        self.update()

    # Sets the local matrix of the transform and sets its transform properties
    def set_matrix(self, matrix):
        self.local_matrix = matrix
        temp_mat = self.local_matrix.copy()

        # Get translation
        self.trans = np.array([temp_mat[0][3], temp_mat[1][3], temp_mat[2][3]])
        temp_mat[0][3] = 0
        temp_mat[1][3] = 0
        temp_mat[2][3] = 0

        # Get scale
        self.scale = np.array([np.linalg.norm(np.array([temp_mat[0][0], temp_mat[1][0], temp_mat[2][0]])),
                               np.linalg.norm(np.array([temp_mat[0][1], temp_mat[1][1], temp_mat[2][1]])),
                               np.linalg.norm(np.array([temp_mat[0][2], temp_mat[1][2], temp_mat[2][2]]))])

        # Get rotation
        temp_mat = temp_mat.dot(np.array([[1 / self.scale[0], 0, 0, 0],
                                          [0, 1 / self.scale[1], 0, 0],
                                          [0, 0, 1 / self.scale[2], 0],
                                          [0, 0, 0, 1]]))
        self.rot = np.array([atan2(temp_mat[2][1], temp_mat[2][2]),
                             atan2(-temp_mat[2][0], sqrt(pow(temp_mat[2][1], 2) + pow(temp_mat[2][2], 2))),
                             atan2(temp_mat[1][0], temp_mat[0][0])])

    # Returns the translation matrix of the translation vector
    def get_trans_mat(self, trans):
        return np.array([[1, 0, 0, trans[0]],
                         [0, 1, 0, trans[1]],
                         [0, 0, 1, trans[2]],
                         [0, 0, 0, 1]])

    # Returns the rotation matrix of the euler rotation vector
    def get_rot_mat(self, rot):
        x_rot_mat = np.array([[1, 0, 0, 0],
                              [0, cos(rot[0]), -sin(rot[0]), 0],
                              [0, sin(rot[0]), cos(rot[0]), 0],
                              [0, 0, 0, 1]])
        y_rot_mat = np.array([[cos(rot[1]), 0, sin(rot[1]), 0],
                              [0, 1, 0, 0],
                              [-sin(rot[1]), 0, cos(rot[1]), 0],
                              [0, 0, 0, 1]])
        z_rot_mat = np.array([[cos(rot[2]), -sin(rot[2]), 0, 0],
                              [sin(rot[2]), cos(rot[2]), 0, 0],
                              [0, 0, 1, 0],
                              [0, 0, 0, 1]])
        return z_rot_mat.dot(y_rot_mat.dot(x_rot_mat))

    # Returns the scale matrix of the scale vector
    def get_scale_mat(self, scale):
        return np.array([[scale[0], 0, 0, 0],
                         [0, scale[1], 0, 0],
                         [0, 0, scale[2], 0],
                         [0, 0, 0, 1]])

    # Returns the local translation of the transform
    def get_translation(self):
        return self.trans

    # Sets the local translation of the transform
    def set_translation(self, translation):
        self.trans = translation
        self.update()

    # Returns the translation of the world transform
    def get_world_translation(self):
        world_trans = self.parent_matrix.dot(np.array([self.trans[0],
                                                       self.trans[1],
                                                       self.trans[2],
                                                       1]))
        return np.array([world_trans[0], world_trans[1], world_trans[2]])

    # Sets the world translation of the transform
    def set_world_translation(self, world_translation):
        # Convert world translation to local
        local_trans_mat = np.linalg.inv(self.parent_matrix).dot(self.get_trans_mat(world_translation))
        self.trans = np.array([local_trans_mat[0][3],
                               local_trans_mat[1][3],
                               local_trans_mat[2][3]])

    # Returns the local rotation of the transform
    def get_rotation(self):
        return self.rot

    # Returns the world rotation of the world transform
    def get_world_rotation(self):
        world_mat = self.parent_matrix.dot(self.get_mat())
        world_transform = Transform()
        world_transform.set_matrix(world_mat)
        return world_transform.get_rotation()

    # Sets the rotation of the transform
    def set_rotation(self, rotation):
        self.rot = rotation
        self.update()

    # Returns the local scale of the transform
    def get_scale(self):
        return self.scale

    # Returns the world scale of the world transform
    def get_world_scale(self):
        world_mat = Transform()
        world_mat.set_matrix(self.get_world_matrix())
        return world_mat.get_scale()

    # Sets the scale of the transform
    def set_scale(self, scale):
        self.scale = scale
        self.update()

    # Sets the world scale of the transform
    def set_world_scale(self, world_scale):
        # Convert world scale to local
        parent_transform = Transform()
        parent_transform.set_matrix(self.parent_matrix)
        scale_mat = np.linalg.inv(self.get_scale_mat(parent_transform.get_scale())).dot(self.get_scale_mat(world_scale))
        self.scale = np.array([scale_mat[0][0], scale_mat[1][1], scale_mat[2][2]])
        self.update()

    # Recalculates the internal local matrix from transform properties
    def recalculate(self):
        scale_mat = self.get_scale_mat(self.scale)
        rot_mat = self.get_rot_mat(self.rot)
        trans_mat = self.get_trans_mat(self.trans)

        self.local_matrix = trans_mat.dot(rot_mat.dot(scale_mat))

    # Returns the local matrix of the transform
    def get_mat(self):
        if self.dirty:
            self.recalculate()
        return self.local_matrix

    # Returns the world matrix of the transform
    def get_world_matrix(self):
        return self.parent_matrix.dot(self.get_mat())

    # Updates the matrix after a change
    def update(self):
        self.recalculate()
        if self.on_matrix_update is not None:
            self.on_matrix_update(self.get_world_matrix())

    # Serializes transform to dictionary
    def to_dict(self):
        return {
            "translation": [self.trans[0].item(), self.trans[1].item(), self.trans[2].item()],
            "rotation": [self.rot[0].item(), self.rot[1].item(), self.rot[2].item()],
            "scale": [self.scale[0].item(), self.scale[1].item(), self.scale[2].item()]
        }

    # Deserializes transform from dictionary
    def load_from_dict(self, dictionary):
        self.trans = np.array(dictionary["translation"])
        self.rot = np.array(dictionary["rotation"])
        self.scale = np.array(dictionary["scale"])
        self.update()
