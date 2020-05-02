"""
Node for Panda3d that renders a floor.
"""
from pathlib import Path
from panda3d.core import GeomVertexFormat, Geom, GeomVertexData, GeomVertexWriter, GeomTriangles, GeomNode, \
    TextureAttrib, RenderState, SamplerState
from direct.showbase.Loader import Loader


class FloorNode(GeomNode):

    def __init__(self, base):
        # Load texture
        tex = Loader(base).loadTexture(Path("resources/checkerboard.png").absolute())
        tex.setMagfilter(SamplerState.FT_nearest)
        tex.setMinfilter(SamplerState.FT_nearest)

        # Set up vertex data
        vdata = GeomVertexData("floor_data", GeomVertexFormat.get_v3t2(), Geom.UHStatic)
        vdata.setNumRows(6)
        vertex = GeomVertexWriter(vdata, "vertex")
        texcoord = GeomVertexWriter(vdata, "texcoord")

        vertex.addData3(-5, -5, 0)
        texcoord.addData3(0, 0, 0)
        vertex.addData3(-5, 5, 0)
        texcoord.addData3(0, 10, 0)
        vertex.addData3(5, 5, 0)
        texcoord.addData3(10, 10, 0)

        vertex.addData3(5, 5, 0)
        texcoord.addData3(10, 10, 0)
        vertex.addData3(5, -5, 0)
        texcoord.addData3(10, 0, 0)
        vertex.addData3(-5, -5, 0)
        texcoord.addData3(0, 0, 0)

        # Create primitive
        prim = GeomTriangles(Geom.UHStatic)
        prim.addVertices(0, 1, 2)
        prim.addVertices(3, 4, 5)
        geom = Geom(vdata)
        geom.add_primitive(prim)

        # Initialize geometry node
        GeomNode.__init__(self, "floor")
        attrib = TextureAttrib.make(tex)
        state = RenderState.make(attrib)
        self.addGeom(geom, state)
