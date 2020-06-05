"""
A selectable mesh.

@author Ben Giacalone
"""
from os import path
from pathlib import Path
import random

import numpy as np
from direct.showbase.Loader import Loader, SamplerState
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTriangles, GeomNode, \
    TextureAttrib, RenderState, LMatrix4f, TransformState, GeomVertexArrayFormat, Shader, Filename, PTA_LMatrix4f

from tools.envedit import helper
from tools.envedit.edenv_component import EComponent
from tools.envedit.gizmos.gizmo import Gizmo


class MeshGizmo(Gizmo):

    def __init__(self, mesh_json=None, object_id=0):
        Gizmo.__init__(self)
        self.matrix = np.identity(4)
        self.object_id = object_id
        self.geom_path = None
        self.bone_mats = None
        self.on_pressed_callback = None
        self.on_released_callback = None

        if mesh_json is not None:
            self.gen_geom(mesh_json)

    # Sets the world matrix of the selectable object
    def set_world_matrix(self, matrix):
        self.matrix = matrix
        panda_mat = LMatrix4f(matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0],
                              matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1],
                              matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2],
                              matrix[0][3], matrix[1][3], matrix[2][3], matrix[3][3])
        self.geom_path.setTransform(TransformState.makeMat(panda_mat))

    def handle_left_pressed(self):
        if self.on_pressed_callback is not None:
            self.on_pressed_callback()

    def set_object_id(self, object_id):
        Gizmo.set_object_id(self, object_id)
        if self.geom_path is not None:
            self.geom_path.set_shader_input("object_id", self.object_id)

    # Destroys the selectable object
    def destroy(self):
        self.geom_path.removeNode()

    # Generates geometry node from JSON
    def gen_geom(self, mesh_json):
        # Create vertex format
        geom_array = GeomVertexArrayFormat()
        geom_array.add_column("vertex", 3, Geom.NTFloat32, Geom.CPoint)
        has_normals = False
        has_texcoords = False
        has_weights = False
        if "normals" in mesh_json:
            geom_array.add_column("normal", 3, Geom.NTFloat32, Geom.CNormal)
            has_normals = True
        if "texcoords" in mesh_json:
            geom_array.add_column("texcoord", 3, Geom.NTFloat32, Geom.CTexcoord)
            has_texcoords = True
        if "weights" in mesh_json:
            geom_array.add_column("joint", 4, Geom.NTUint8, Geom.CIndex)
            geom_array.add_column("weight", 4, Geom.NTFloat32, Geom.COther)
            has_weights = True
        geom_format = GeomVertexFormat()
        geom_format.add_array(geom_array)
        geom_format = GeomVertexFormat.register_format(geom_format)

        # Set up vertex data
        vdata = GeomVertexData(str(random.randint(0, 255)) + "_vdata", geom_format, Geom.UHStatic)
        vcount = len(mesh_json["vertices"]) // 3
        vdata.setNumRows(vcount)
        vertex = GeomVertexWriter(vdata, "vertex")

        for i in range(vcount):
            vertex.addData3(mesh_json["vertices"][3 * i],
                            mesh_json["vertices"][3 * i + 1],
                            mesh_json["vertices"][3 * i + 2])
        if has_normals:
            normal = GeomVertexWriter(vdata, "normal")
            for i in range(vcount):
                normal.addData3(mesh_json["normals"][3 * i],
                                mesh_json["normals"][3 * i + 1],
                                mesh_json["normals"][3 * i + 2])
        if has_texcoords:
            texcoord = GeomVertexWriter(vdata, "texcoord")
            for i in range(vcount):
                texcoord.addData2(mesh_json["texcoords"][2 * i],
                                  mesh_json["texcoords"][2 * i + 1])
        if has_weights:
            joint = GeomVertexWriter(vdata, "joint")
            weight = GeomVertexWriter(vdata, "weight")
            for i in range(vcount):
                joint_count = len(mesh_json["joints"][i])
                joint.addData4(0 if joint_count < 1 else mesh_json["joints"][i][0],
                               0 if joint_count < 2 else mesh_json["joints"][i][1],
                               0 if joint_count < 3 else mesh_json["joints"][i][2],
                               0 if joint_count < 4 else mesh_json["joints"][i][3])
                weight.addData4(0 if joint_count < 1 else mesh_json["weights"][i][0],
                                0 if joint_count < 2 else mesh_json["weights"][i][1],
                                0 if joint_count < 3 else mesh_json["weights"][i][2],
                                0 if joint_count < 4 else mesh_json["weights"][i][3])

        # Create primitive
        prim = GeomTriangles(Geom.UHStatic)
        for i in range(vcount // 3):
            prim.addVertices(3 * i, 3 * i + 1, 3 * i + 2)
        geom = Geom(vdata)
        geom.add_primitive(prim)

        # Load texture
        tex = None
        if "texture" in mesh_json:
            tex = Loader(EComponent.base).loadTexture((Path("resources") / mesh_json["texture"]).absolute())
            tex.setMagfilter(SamplerState.FT_nearest)
            tex.setMinfilter(SamplerState.FT_nearest)

        # Create new geometry node
        geom_node = GeomNode(str(random.randint(0, 255)) + "_node")
        if tex is None:
            geom_node.addGeom(geom)
        else:
            attrib = TextureAttrib.make(tex)
            state = RenderState.make(attrib)
            geom_node.addGeom(geom, state)
        if EComponent.panda_root_node is not None:
            self.geom_path = EComponent.panda_root_node.attach_new_node(geom_node)
            self.geom_path.set_shader_input("object_id", self.object_id)

        # Set shader
        if has_weights:
            self.geom_path.setTag("shader type", "skinned")
            bone_mats = PTA_LMatrix4f()
            for _ in range(100):
                bone_mats.push_back(helper.np_mat4_to_panda(np.identity(4)))
            self.geom_path.set_shader_input(f"boneMats", bone_mats)

    # Returns the geometry node path
    def get_geom(self):
        return self.geom_path

    # Sets the bone matrices
    def set_bone_matrices(self, bone_mats):
        self.geom_path.set_shader_input(f"boneMats", bone_mats)
