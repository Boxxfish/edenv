"""
Represents a component.
Components are backed by a script that specifies its properties.

@author Ben Giacalone
"""
import pkgutil
from pathlib import Path
import importlib
from tools.envedit.property_type import PropertyType
from tools.run.physics import Physics


class EComponent:
    panda_root_node = None
    physics_world = None
    base = None

    def __init__(self, name="", property_types={}):
        self.name = name
        self.property_types = property_types
        self.property_vals = {}
        self.node = None
        self.script_path = None
        self.physics = Physics(EComponent.physics_world)
        self.component_update_callback = None       # Called when component modifies

    # Returns the default value of the field type
    @staticmethod
    def get_default_value(property_type):
        if property_type == PropertyType.INT:
            return "0"
        elif property_type == PropertyType.FLOAT:
            return "0.0"
        elif property_type == PropertyType.BOOL:
            return "True"
        elif property_type == PropertyType.STRING:
            return "Text"
        elif property_type == PropertyType.FILE:
            return "File Path"
        elif property_type == PropertyType.ARRAY:
            return [""]
        elif property_type == PropertyType.VECTOR3:
            return ["0", "0", "0"]
        elif property_type == PropertyType.NODE:
            return "0000000000000000"

    # Returns a dictionary with the values of the component
    def to_dict(self):
        component_dict = {}
        component_dict["script_path"] = self.script_path
        component_dict["values"] = self.property_vals
        return component_dict

    # Called when component must change and node isn't selected
    def on_gui_change(self):
        pass

    # Called when component must change and node is selected
    def on_gui_change_selected(self):
        pass

    # Called every frame
    def on_gui_update(self):
        pass

    # Called when component or node is removed
    def on_gui_remove(self):
        pass

    # Called at the beginning of the trial
    def start(self):
        pass

    # Returns the component from a script path
    @staticmethod
    def from_script(script_path):
        module_name = script_path.split(".")[-1].title()
        module_name = module_name.replace("_", "")

        # Check if module exists in path
        script_spec = importlib.util.find_spec(script_path)
        if script_spec is not None:
            # Import the first class in the script path
            module = __import__(script_path, fromlist=[module_name])
            component_class = getattr(module, module_name)
            new_component = component_class()
            new_component.script_path = script_path

            # Set properties of new component
            new_component.name = module_name
            new_component.property_types = component_class.get_properties()
            new_component.property_vals = {}
            for property in new_component.property_types:
                new_component.property_vals[property] = EComponent.get_default_value(new_component.property_types[property])
            return new_component

        raise Exception(f"No module \"{script_path}\" exists")

    # Creates a new component from a dictionary
    @staticmethod
    def load_from_dict(component_dict):
        new_component = EComponent.from_script(component_dict["script_path"])
        new_component.property_vals = component_dict["values"]
        property_types = new_component.get_properties()
        for property in property_types:
            if property not in new_component.property_vals:
                property_val = EComponent.get_default_value(property_types[property])
                new_component.property_vals[property] = property_val
        return new_component
