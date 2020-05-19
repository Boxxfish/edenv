"""
Renders a mesh.

"""
import json
from pathlib import Path

from direct.showbase.Loader import Loader
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTriangles, GeomNode, \
    TextureAttrib, RenderState, SamplerState, TransformState, LMatrix4f
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType


class MeshGraphic(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.mesh = None
        self.geom_path = None
        
    # Called by scene editor to get this component's properties
    @staticmethod
    def get_properties():
        return {"mesh": PropertyType.FILE}

    # Called when component property is changed
    def on_gui_change(self, properties):
        # Only change mesh if it's different
        if not hasattr(self, "mesh") or self.mesh is not properties["mesh"]:

            # If a geom_node already exists, remove it
            if hasattr(self, "geom_path") and self.geom_path is not None:
                self.geom_path.removeNode()

            # Open mesh file
            self.mesh = properties["mesh"]
            mesh_path = Path("resources") / (self.mesh + ".json")
            if not mesh_path.exists():
                return
            with open(mesh_path, "r") as file:
                mesh_json = json.load(file)

                # Load texture
                tex = Loader(EComponent.base).loadTexture((Path("resources") / mesh_json["texture"]).absolute())
                tex.setMagfilter(SamplerState.FT_nearest)
                tex.setMinfilter(SamplerState.FT_nearest)

                # Set up vertex data
                vdata = GeomVertexData(self.mesh + "_vdata", GeomVertexFormat.get_v3n3t2(), Geom.UHStatic)
                vcount = len(mesh_json["vertices"]) // 3
                vdata.setNumRows(vcount)
                vertex = GeomVertexWriter(vdata, "vertex")
                normal = GeomVertexWriter(vdata, "normal")
                texcoord = GeomVertexWriter(vdata, "texcoord")

                for i in range(vcount):
                    vertex.addData3(mesh_json["vertices"][3 * i], mesh_json["vertices"][3 * i + 1], mesh_json["vertices"][3 * i + 2])
                    normal.addData3(mesh_json["normals"][3 * i], mesh_json["normals"][3 * i + 1], mesh_json["normals"][3 * i + 2])
                    texcoord.addData2(mesh_json["texcoords"][2 * i], mesh_json["texcoords"][2 * i + 1])

                # Create primitive
                prim = GeomTriangles(Geom.UHStatic)
                for i in range(vcount // 3):
                    prim.addVertices(3 * i, 3 * i + 1, 3 * i + 2)
                geom = Geom(vdata)
                geom.add_primitive(prim)

                # Create new geometry node
                geom_node = GeomNode(self.mesh + "_node")
                attrib = TextureAttrib.make(tex)
                state = RenderState.make(attrib)
                geom_node.addGeom(geom, state)
                self.geom_path = EComponent.panda_root_node.attach_new_node(geom_node)

        # Set the transform of the geometry node
        if hasattr(self, "geom_path") and self.geom_path is not None:
            mat = self.node.transform.get_world_matrix()
            panda_mat = LMatrix4f(mat[0][0], mat[1][0], mat[2][0], mat[3][0],
                                  mat[0][1], mat[1][1], mat[2][1], mat[3][1],
                                  mat[0][2], mat[1][2], mat[2][2], mat[3][2],
                                  mat[0][3], mat[1][3], mat[2][3], mat[3][3])
            self.geom_path.setTransform(TransformState.makeMat(panda_mat))

    # Called when the component is removed
    def on_gui_remove(self, properties):
        if hasattr(self, "geom_path") and self.geom_path is not None:
            self.geom_path.removeNode()

    # Called when the scene starts
    def start(self, properties):
        self.mesh = properties["mesh"]
