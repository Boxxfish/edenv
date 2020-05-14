"""
Represents a component.
Components are backed by a script that specifies its properties.

@author Ben Giacalone
"""
from tools.envedit.property_type import PropertyType


class EComponent:

    def __init__(self, name="", property_types={}):
        self.name = name
        self.property_types = property_types
        self.property_vals = {}
        self.script_path = None

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

    # Sets the component's script and its property types
    def set_script(self, script_path):
        self.script_path = script_path

        # Import the first class in the script path
        module_name = script_path.split(".")[-1].title()
        module_name = module_name.replace("_", "")
        module = __import__(script_path, fromlist=[module_name])
        component_class = getattr(module, module_name)

        # Set properties of EComponent
        self.name = module_name
        self.property_types = component_class.get_properties()
        self.property_vals = {}
        for property in self.property_types:
            self.property_vals[property] = EComponent.get_default_value(self.property_types[property])

    # Returns a dictionary with the values of the component
    def to_dict(self):
        component_dict = {}
        component_dict["script_path"] = self.script_path
        component_dict["values"] = self.property_vals
        return component_dict

    # Loads the values from a dictionary into itself
    def load_from_dict(self, component_dict):
        self.set_script(component_dict["script_path"])
        self.property_vals = component_dict["values"]
