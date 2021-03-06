"""
A wireframe circle gizmo.

@author Ben Giacalone
"""
import json
from os import path
from pathlib import Path
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo


class WireCircleGizmo(MeshGizmo):
    def __init__(self):
        MeshGizmo.__init__(self)
        self.color = (1.0, 1.0, 1.0, 1.0)

        # Load cube mesh file
        circle_json = None
        circle_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/meshes/circle.json"
        with open(circle_path, "r") as file:
            circle_json = json.load(file)

        # Generate mesh (renders on top of everything else)
        MeshGizmo.gen_geom(self, circle_json)
        self.get_geom().setColor(self.color)
        self.get_geom().setBin("fixed", 0)
        self.get_geom().setDepthTest(False)
        self.get_geom().setLightOff()
        self.get_geom().setTwoSided(True)
        self.get_geom().setRenderModeWireframe()

    # Sets circle's color
    def set_color(self, color):
        self.color = color
        self.get_geom().setColor(self.color)
