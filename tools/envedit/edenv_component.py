"""
Represents a component.
Components are backed by a script that specifies its properties.

@author Ben Giacalone
"""


class EComponent:

    def __init__(self, name="", properties={}):
        self.name = name
        self.properties = properties

    def set_script(self, script_path):
        # Import the first class in the script path
        module_name = script_path.split(".")[-1].title()
        module = __import__(script_path, fromlist=[module_name])
        component_class = getattr(module, module_name)

        # Set properties of EComponent
        self.name = module_name
        self.properties = component_class.get_properties()
