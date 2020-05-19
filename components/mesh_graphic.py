"""
Renders a mesh.

"""
import json
from pathlib import Path

from direct.showbase.Loader import Loader
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTriangles, GeomNode, \
    TextureAttrib, RenderState, SamplerState
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
            vdata = GeomVertexData(self.mesh + "_vdata", GeomVertexFormat.get_v3t2(), Geom.UHStatic)
            vcount = len(mesh_json["vertices"]) // 3
            vdata.setNumRows(vcount)
            vertex = GeomVertexWriter(vdata, "vertex")
            texcoord = GeomVertexWriter(vdata, "texcoord")

            for i in range(vcount):
                vertex.addData3(mesh_json["vertices"][3 * i], mesh_json["vertices"][3 * i + 1], mesh_json["vertices"][3 * i + 2])
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
            self.geom_path.setPos(self.node.transform.trans[0], self.node.transform.trans[1], self.node.transform.trans[2])
            self.geom_path.setHpr(self.node.transform.rot[0], self.node.transform.rot[1], self.node.transform.rot[2])
            self.geom_path.setScale(self.node.transform.scale[0], self.node.transform.scale[1], self.node.transform.scale[2])

    # Called when the component is removed
    def on_gui_remove(self, properties):
        if hasattr(self, "geom_path") and self.geom_path is not None:
            self.geom_path.removeNode()

    # Called when the scene starts
    def start(self, properties):
        self.mesh = properties["mesh"]
