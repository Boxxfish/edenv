"""
Indexes nodes for skinned meshes.

"""
import numpy as np
from panda3d.core import PTA_LMatrix4f

from tools.envedit import helper
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType
from tools.run.event import handler


class Armature(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.nodes = []
        self.bone_mats = PTA_LMatrix4f()
        self.bind_mats = []

    # Called by scene editor to get this component's properties
    @staticmethod
    def get_properties():
        return {"nodes": PropertyType.ARRAY,
                "bind_matrices": PropertyType.ARRAY}

    def on_gui_change(self):
        self.bind_mats.clear()
        for bind_matrix in self.property_vals["bind_matrices"]:
            mat = np.identity(4)
            elements = bind_matrix.split(",")
            for x in range(4):
                for y in range(4):
                    mat[y][x] = float(elements[y * 4 + x])
            self.bind_mats.append(mat)

    def on_gui_change_selected(self):
        # Update node list
        nodes_len = len(self.property_vals["nodes"])
        self.nodes = [None for _ in range(nodes_len)]
        for i in range(nodes_len):
            node = self.node.find_child_by_name(self.property_vals["nodes"][i])
            if node is not None:
                self.nodes[i] = node
            else:
                self.nodes[i] = None

    def on_gui_update(self):
        nodes_len = len(self.property_vals["nodes"])
        self.nodes = [None for _ in range(nodes_len)]
        for i in range(nodes_len):
            node = self.node.find_child_by_name(self.property_vals["nodes"][i])
            if node is not None:
                self.nodes[i] = node
            else:
                self.nodes[i] = None
        self.update_bone_matrices()

    def start(self):
        # Set up bind matrices
        for bind_matrix in self.property_vals["bind_matrices"]:
            mat = np.identity(4)
            elements = bind_matrix.split(",")
            for x in range(4):
                for y in range(4):
                    mat[y][x] = float(elements[y * 4 + x])
            self.bind_mats.append(mat)

        # Save nodes
        nodes_len = len(self.property_vals["nodes"])
        self.nodes = [None for _ in range(nodes_len)]
        for i in range(nodes_len):
            node = self.node.find_child_by_name(self.property_vals["nodes"][i])
            if node is not None:
                self.nodes[i] = node
            else:
                self.nodes[i] = None

        # Set up bone matrices
        self.update_bone_matrices()

    @handler()
    def handle_update(self):
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            bind_mat = self.bind_mats[i]
            self.bone_mats.setElement(i, helper.np_mat4_to_panda(node.transform.get_world_matrix().dot(bind_mat)))

    # Updates bone matrices
    def update_bone_matrices(self):
        self.bone_mats = PTA_LMatrix4f()
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            bind_mat = self.bind_mats[i]
            if node is not None:
                self.bone_mats.push_back(helper.np_mat4_to_panda(node.transform.get_world_matrix().dot(bind_mat)))
            else:
                self.bone_mats.push_back(helper.np_mat4_to_panda(np.identity(4)))
