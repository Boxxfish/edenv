"""
Renders a mesh.

"""
import json
from pathlib import Path
from tools.envedit.edenv_component import EComponent
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

    # Called when component property is changed
    def on_gui_change(self, properties):
        # Only change mesh if it's different
        if not hasattr(self, "mesh") or self.mesh is not properties["mesh"]:

            # If a selectable object already exists, remove it
            if hasattr(self, "selectable_object") and self.selectable_object is not None:
                self.selectable_object.destroy()
                self.selectable_object = None

            # Open mesh file
            self.mesh = properties["mesh"]
            mesh_path = Path("resources") / (self.mesh + ".json")
            if not mesh_path.exists():
                return
            with open(mesh_path, "r") as file:
                mesh_json = json.load(file)
                self.mesh_gizmo = MeshGizmo(mesh_json)
                self.mesh_gizmo.on_pressed_callback = self.pressed_callback
                self.mesh_gizmo.on_deselect_callback = self.deselected_callback
                GizmoSystem.add_gizmo(self.mesh_gizmo)

        # Change selected object's matrix
        if hasattr(self, "mesh_gizmo") and self.mesh_gizmo is not None:
            self.mesh_gizmo.set_world_matrix(self.node.transform.get_world_matrix())

    # Called when the component is removed
    def on_gui_remove(self, properties):
        if hasattr(self, "mesh_gizmo") and self.mesh_gizmo is not None:
            self.mesh_gizmo.destroy()
            GizmoSystem.remove_gizmo(self.mesh_gizmo)

    # Called when the node is selected
    def on_node_selected(self):
        GizmoSystem.set_focus(self.mesh_gizmo)
        self.mesh_gizmo.get_geom().setColor((1, 1, 0, 1))

    # Called when node is deselected
    def on_node_deselected(self):
        self.mesh_gizmo.get_geom().setColor((1, 1, 1, 1))

    # Called when the scene starts
    def start(self, properties):
        self.mesh = properties["mesh"]
