"""
Represents a component.
Components are backed by a script that specifies its properties.

@author Ben Giacalone
"""
from tools.envedit.property_type import PropertyType


class EComponent:
    panda_root_node = None
    base = None

    def __init__(self, name="", property_types={}):
        self.name = name
        self.property_types = property_types
        self.property_vals = {}
        self.node = None
        self.script_path = None
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
            return [0, 0, 0]

    # Returns a dictionary with the values of the component
    def to_dict(self):
        component_dict = {}
        component_dict["script_path"] = self.script_path
        component_dict["values"] = self.property_vals
        return component_dict

    def on_gui_change(self):
        pass

    def on_gui_change_selected(self):
        pass

    def on_gui_update(self):
        pass

    def on_gui_remove(self):
        pass

    # Returns the component from a script path
    @staticmethod
    def from_script(script_path):
        # Import the first class in the script path
        module_name = script_path.split(".")[-1].title()
        module_name = module_name.replace("_", "")
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

    # Creates a new component from a dictionary
    @staticmethod
    def load_from_dict(component_dict):
        new_component = EComponent.from_script(component_dict["script_path"])
        new_component.property_vals = component_dict["values"]
        return new_component
