"""
Handles hot reloading component list.

@author Ben Giacalone
"""
import sys
from pathlib import Path

import yaml
from direct.showbase import DirectObject


class ComponentReloader(DirectObject.DirectObject):

    def __init__(self, component_viewer):
        self.component_viewer = component_viewer
        self.accept("window-event", self.handle_window)

    def handle_window(self, window):
        # Reset component list from project.yaml
        config_path = Path("project.yaml")
        config = None
        if not config_path.exists():
            sys.stderr.write("Error: Could not find project.yaml.")
            return
        with open("project.yaml", "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.component_viewer.set_components(config["components"])