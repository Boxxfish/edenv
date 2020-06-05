"""
Helper functions and values for envedit.

@author Ben Giacalone
"""
import numpy as np
from panda3d.core import LMatrix4f, LVector3f


def panda_mat4_to_np(panda_mat):
    return np.array([[panda_mat[0][0], panda_mat[1][0], panda_mat[2][0], panda_mat[3][0]],
                     [panda_mat[0][1], panda_mat[1][1], panda_mat[2][1], panda_mat[3][1]],
                     [panda_mat[0][2], panda_mat[1][2], panda_mat[2][2], panda_mat[3][2]],
                     [panda_mat[0][3], panda_mat[1][3], panda_mat[2][3], panda_mat[3][3]]])


def np_mat4_to_panda(np_mat):
    return LMatrix4f(np_mat[0][0], np_mat[1][0], np_mat[2][0], np_mat[3][0],
                     np_mat[0][1], np_mat[1][1], np_mat[2][1], np_mat[3][1],
                     np_mat[0][2], np_mat[1][2], np_mat[2][2], np_mat[3][2],
                     np_mat[0][3], np_mat[1][3], np_mat[2][3], np_mat[3][3])


def panda_vec3_to_np(panda_vec):
    return np.array([panda_vec[0], panda_vec[1], panda_vec[2]])


def np_vec3_to_panda(np_vec):
    return LVector3f(np_vec[0], np_vec[1], np_vec[2])
