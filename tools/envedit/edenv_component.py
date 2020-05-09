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
        # TODO: Analyze script and set properties
        pass
