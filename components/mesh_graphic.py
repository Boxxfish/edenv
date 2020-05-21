"""
Renders a mesh.

"""
import json
from pathlib import Path
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType
from tools.envedit.selectable_object import SelectableObject


class MeshGraphic(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.mesh = None
        self.geom_path = None
        self.selectable_object = None
        
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
                self.selectable_object = SelectableObject(mesh_json)
                self.selectable_object.on_pressed = self.pressed_callback

        # Change selected object's matrix
        if hasattr(self, "selectable_object") and self.selectable_object is not None:
            self.selectable_object.set_world_matrix(self.node.transform.get_world_matrix())

    # Called when the component is removed
    def on_gui_remove(self, properties):
        if hasattr(self, "selectable_object") and self.selectable_object is not None:
            self.selectable_object.destroy()

    # Called when the component is pressed
    def on_pressed(self):
        pass

    # Called when the scene starts
    def start(self, properties):
        self.mesh = properties["mesh"]
