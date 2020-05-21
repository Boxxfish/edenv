"""
A selectable object that can be picked by the object selector.

@author Ben Giacalone
"""
from pathlib import Path
import random

import numpy as np
from direct.showbase.Loader import Loader, SamplerState
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTriangles, GeomNode, \
    TextureAttrib, RenderState, LMatrix4f, TransformState
from tools.envedit.edenv_component import EComponent
from tools.envedit.object_selector import ObjectSelector


class SelectableObject:

    def __init__(self, mesh_json=None):
        self.matrix = np.identity(4)
        self.object_id = self.object_id = ObjectSelector.gen_obj_id(self.pressed_callback, self.released_callback)
        self.geom_path = None
        self.on_pressed = None
        self.on_released = None

        if mesh_json is not None:
            self.gen_geom(mesh_json)

    # Generates geometry node from JSON
    def gen_geom(self, mesh_json):
        # Load texture
        tex = Loader(EComponent.base).loadTexture((Path("resources") / mesh_json["texture"]).absolute())
        tex.setMagfilter(SamplerState.FT_nearest)
        tex.setMinfilter(SamplerState.FT_nearest)

        # Set up vertex data
        vdata = GeomVertexData(str(random.randint(0, 255)) + "_vdata", GeomVertexFormat.get_v3n3t2(), Geom.UHStatic)
        vcount = len(mesh_json["vertices"]) // 3
        vdata.setNumRows(vcount)
        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")
        texcoord = GeomVertexWriter(vdata, "texcoord")

        for i in range(vcount):
            vertex.addData3(mesh_json["vertices"][3 * i], mesh_json["vertices"][3 * i + 1],
                            mesh_json["vertices"][3 * i + 2])
            normal.addData3(mesh_json["normals"][3 * i], mesh_json["normals"][3 * i + 1],
                            mesh_json["normals"][3 * i + 2])
            texcoord.addData2(mesh_json["texcoords"][2 * i], mesh_json["texcoords"][2 * i + 1])

        # Create primitive
        prim = GeomTriangles(Geom.UHStatic)
        for i in range(vcount // 3):
            prim.addVertices(3 * i, 3 * i + 1, 3 * i + 2)
        geom = Geom(vdata)
        geom.add_primitive(prim)

        # Create new geometry node
        geom_node = GeomNode(str(random.randint(0, 255)) + "_node")
        attrib = TextureAttrib.make(tex)
        state = RenderState.make(attrib)
        geom_node.addGeom(geom, state)
        self.geom_path = EComponent.panda_root_node.attach_new_node(geom_node)
        self.geom_path.set_shader_input("object_id", self.object_id)

    # Returns the geometry node path
    def get_geom(self):
        return self.geom_path

    # Returns the object ID
    def get_object_id(self):
        return self.object_id

    # Sets the object ID
    def set_object_id(self, object_id):
        self.object_id = object_id

    # Sets the world matrix of the selectable object
    def set_world_matrix(self, matrix):
        self.matrix = matrix
        panda_mat = LMatrix4f(matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0],
                              matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1],
                              matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2],
                              matrix[0][3], matrix[1][3], matrix[2][3], matrix[3][3])
        self.geom_path.setTransform(TransformState.makeMat(panda_mat))

    # Destroys the selectable object
    def destroy(self):
        ObjectSelector.free_obj_id(self.object_id)
        self.geom_path.removeNode()

    # Handles the object being pressed
    def pressed_callback(self):
        if self.on_pressed is not None:
            self.on_pressed()

    # Handles the object being released
    def released_callback(self):
        if self.on_released is not None:
            self.on_released()
