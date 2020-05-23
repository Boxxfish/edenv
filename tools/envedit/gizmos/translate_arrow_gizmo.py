"""
An arrow gizmo for translation.

@author Ben Giacalone
"""
import json
import math
from os import path
from pathlib import Path

from panda3d.core import Filename, Shader, LVector4f

from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo
from tools.envedit.transform import Transform


class TranslateArrowGizmo(MeshGizmo):

    def __init__(self):
        MeshGizmo.__init__(self)
        self.color = (1.0, 1.0, 1.0, 1.0)

        # Load arrow mesh file
        arrow_json = None
        arrow_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/meshes/translate_arrow.json"
        with open(arrow_path, "r") as file:
            arrow_json = json.load(file)

        # Generate mesh
        MeshGizmo.gen_geom(self, arrow_json)
        self.get_geom().setColor(self.color)

    def set_object_id(self, object_id):
        MeshGizmo.set_object_id(self, object_id)

    # Sets arrow's color
    def set_color(self, color):
        self.color = color
        self.get_geom().setColor(self.color)

    def handle_left_pressed(self):
        GizmoSystem.set_drag(self)
        self.get_geom().setColor(self.color[0] - 0.2, self.color[1] - 0.2, self.color[2] - 0.2, self.color[3])

    def handle_left_released(self):
        self.get_geom().setColor(self.color)

    def handle_drag(self, screen_x, screen_y):
        print(f"{screen_x}, {screen_y}")

    def handle_drag_stop(self):
        self.get_geom().setColor(self.color)

