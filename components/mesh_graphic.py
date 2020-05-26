"""
Renders a mesh.

"""
import json
from pathlib import Path
from tools.envedit.edenv_component import EComponent
from tools.envedit.envedit_data import EnveditData
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.gizmos.mesh_gizmo import MeshGizmo
from tools.envedit.property_type import PropertyType


class MeshGraphic(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.mesh = None
        self.mesh_gizmo = None

    # Called by scene editor to get this component's properties
    @staticmethod
    def get_properties():
        return {"mesh": PropertyType.FILE}

    def on_gui_change(self):
        # Change color
        if self.mesh_gizmo is not None:
            self.mesh_gizmo.get_geom().setColor((1, 1, 1, 1))

        # Only change mesh if it's different
        if self.mesh is not self.property_vals["mesh"]:

            # If a selectable object already exists, remove it
            if self.mesh_gizmo is not None:
                self.mesh_gizmo.destroy()
                self.mesh_gizmo = None

            # Open mesh file
            self.mesh = self.property_vals["mesh"]
            mesh_path = Path("resources") / (self.mesh + ".json")
            if not mesh_path.exists():
                return
            with open(mesh_path, "r") as file:
                mesh_json = json.load(file)
                self.mesh_gizmo = MeshGizmo(mesh_json)
                self.mesh_gizmo.on_pressed_callback = self.pressed_callback
                GizmoSystem.add_gizmo(self.mesh_gizmo)

        # Change object's matrix
        if self.mesh_gizmo is not None:
            self.mesh_gizmo.set_world_matrix(self.node.transform.get_world_matrix())

    def on_gui_change_selected(self):
        # Change color
        if self.mesh_gizmo is not None:
            self.mesh_gizmo.get_geom().setColor((1, 1, 0, 1))

        # Change selected object's matrix
        if self.mesh_gizmo is not None:
            self.mesh_gizmo.set_world_matrix(self.node.transform.get_world_matrix())

    # Called when the component is removed
    def on_gui_remove(self, properties):
        if self.mesh_gizmo is not None:
            self.mesh_gizmo.destroy()
            GizmoSystem.remove_gizmo(self.mesh_gizmo)

    # Called when the scene starts
    def start(self, properties):
        self.mesh = properties["mesh"]

    # Called when mesh gizmo is pressed
    def pressed_callback(self):
        EnveditData.envedit_data.set_target_node(self.node)
