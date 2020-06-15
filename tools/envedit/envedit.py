"""
Environment editor for EDEnv.

@author Ben Giacalone
"""
from os import path
from pathlib import Path
import sys
from tkinter import filedialog

import numpy as np
import yaml
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Shader, Filename, PTA_LMatrix4f, PandaNode, DirectionalLight, NodePath, WindowProperties, \
    LVector3f
from tools.envedit import helper
from tools.envedit.camera_controller import CameraController
from tools.envedit.center_panel import CenterPanel
from tools.envedit.component_viewer import ComponentViewer
from tools.envedit.edenv_component import EComponent
from tools.envedit.floor_node import FloorNode
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.graph_node import GraphNode
from tools.envedit.graph_viewer import GraphViewer
from tools.envedit.envedit_data import EnveditData
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_font_loader import GUIFontLoader
from tools.envedit.gui.gui_system import GUISystem
from tools.envedit.toolbar import Toolbar
import tkinter as tk


class EnvEdit(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Initial scene setup
        self.disableMouse()
        self.setBackgroundColor(0.15, 0.15, 0.15, 1)
        EComponent.panda_root_node = self.render.attach_new_node(PandaNode("Root"))
        EComponent.base = self

        # Attach a directional light to the camera
        self.dir_light = DirectionalLight("cam_dir_light")
        dir_light_path = self.camera.attach_new_node(self.dir_light)
        EComponent.panda_root_node.setLight(dir_light_path)

        # Set up scene data
        self.envedit_data = EnveditData()
        self.envedit_data.update_callback = self.update_gui
        self.envedit_data.scene_root = GraphNode("Scene Root", [])
        self.envedit_data.panda_root_node = EComponent.panda_root_node

        # Read the project config file
        config_path = Path("project.yaml")
        config = None
        if not config_path.exists():
            sys.stderr.write("Error: Could not find project.yaml.")
            return
        with open("project.yaml", "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.envedit_data.project_name = config["project"]

        # Set up GUI system
        self.gui_system = GUISystem(self)
        GUIFontLoader.base = self
        GUISystem.fonts["default"] = GUIFontLoader.load_font("open-sans/OpenSans-Regular.ttf")
        GUISystem.fonts["default_bold"] = GUIFontLoader.load_font("open-sans/OpenSans-Bold.ttf")
        GUISystem.fonts["default_light"] = GUIFontLoader.load_font("open-sans/OpenSans-Light.ttf")
        window_layout = GUIDockLayout()
        self.gui_system.window.set_child(window_layout)

        # Set up Tkinter (for file dialogs)
        root = tk.Tk()
        root.withdraw()

        # Set up gizmo system
        self.gizmo_system = GizmoSystem(self, self.envedit_data)

        # Add floor
        self.floor_node = FloorNode(self)
        floor_path = self.render.attach_new_node(self.floor_node)
        floor_path.setTwoSided(True)
        floor_path.set_shader_input("object_id", 0)

        # Add camera controller
        self.cam_controller = CameraController(self, self.render, self.camera)

        # Add graph viewer
        self.graph_viewer = GraphViewer()
        window_layout.set_child_dock(self.graph_viewer, GUIDockLayout.LEFT)
        self.graph_viewer.set_envedit_data(self.envedit_data)

        # Add component viewer
        self.component_viewer = ComponentViewer()
        window_layout.set_child_dock(self.component_viewer, GUIDockLayout.RIGHT)
        self.component_viewer.set_envedit_data(self.envedit_data)
        self.component_viewer.set_components(config["components"])

        # Add toolbar
        self.toolbar = Toolbar()
        window_layout.set_child_dock(self.toolbar, GUIDockLayout.TOP)
        self.toolbar.set_envedit_data(self.envedit_data)

        # Add empty center panel
        self.center_panel = CenterPanel(self.cam_controller)
        window_layout.set_child_dock(self.center_panel, GUIDockLayout.CENTER)

        # Add task to update nodes
        self.add_task(self.update_nodes)

        # Set up event handlers for key combinations
        self.accept("control-n", self.handle_new)
        self.accept("control-o", self.handle_open)
        self.accept("control-s", self.handle_save)

        self.update_gui()

    # Updates the GUI after a change to the scene
    def update_gui(self):
        # Update scene graph viewer and component viewer
        self.graph_viewer.update_viewer()
        self.component_viewer.update_viewer()

        # Update window title
        dirty_marker = "*" if self.envedit_data.dirty else ""
        window_properties = WindowProperties()
        if self.envedit_data.save_path is not None:
            window_properties.setTitle(
                f"{dirty_marker}{Path(self.envedit_data.save_path).name} | {self.envedit_data.project_name}")
        else:
            window_properties.setTitle(f"{dirty_marker}new_scene | {self.envedit_data.project_name}")
        self.win.requestProperties(window_properties)

    # Updates the nodes every frame
    def update_nodes(self, task):
        self.update_node(self.envedit_data.scene_root)
        return Task.cont

    # Recursive function to update nodes
    def update_node(self, node):
        node.component_gui_update()
        for child in node.children:
            self.update_node(child)

    def handle_new(self):
        # Reset the scene root
        self.envedit_data.scene_root.clear()
        self.envedit_data.update()

        # TODO: When scene data is reset, if the dirt flag is set, bring up save dialog

    def handle_open(self):
        # Open file dialog
        filetypes = [("JSON", "*.json")]
        file_path = filedialog.askopenfilename(filetypes=filetypes, defaultextension=filetypes)

        # Load file
        if file_path != "":
            for child in self.envedit_data.panda_root_node.children:
                NodePath(child).removeNode()
            self.envedit_data.load(file_path)

        # TODO: When scene data is loaded, if the dirt flag is set, bring up save dialog

    def handle_save(self):
        if self.envedit_data.save_path is None:
            # Open file dialog
            filetypes = [("JSON", "*.json")]
            file_path = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes)

            # Save file
            if file_path != "":
                self.envedit_data.save(file_path)
        else:
            self.envedit_data.save()


def main():
    app = EnvEdit()
    app.run()


if __name__ == "__main__":
    main()
