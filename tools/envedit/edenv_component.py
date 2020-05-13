"""
Represents a component.
Components are backed by a script that specifies its properties.

@author Ben Giacalone
"""


class EComponent:

    def __init__(self, name="", property_types={}):
        self.name = name
        self.property_types = property_types
        self.property_vals = None
        self.script_path = None

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

    # Returns a dictionary with the values of the component
    def to_dict(self):
        component_dict = {}
        component_dict["script_path"] = self.script_path
        component_dict["values"] = self.property_vals
        return component_dict
