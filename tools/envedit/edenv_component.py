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
        self.component_class = None

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
        self.component_class = getattr(module, module_name)

        # Set properties of EComponent
        self.name = module_name
        self.property_types = self.component_class.get_properties()
        self.property_vals = {}
        for property in self.property_types:
            self.property_vals[property] = EComponent.get_default_value(self.property_types[property])
        self.property_changed()

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
        self.property_changed()

    # Called when a property value has changed
    def property_changed(self):
        if self.node is not None and self.component_class is not None:
            self.component_class.on_gui_change(self, self.property_vals)

    # Called when the component is removed
    def component_removed(self, properties):
        self.component_class.on_gui_remove(self, self.property_vals)

    # Called when node is pressed
    def pressed_callback(self):
        self.node.pressed_callback(self.node)
        self.component_class.on_node_selected(self)

    # Called when node is deselected
    def deselected_callback(self):
        self.component_class.on_node_deselected(self)

    def on_gui_change(self, properties):
        pass

    def on_gui_remove(self, properties):
        pass

    def on_node_selected(self):
        pass

    def on_node_deselected(self):
        pass
