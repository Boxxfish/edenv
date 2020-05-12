"""
Environment editor for EDEnv.

@author Ben Giacalone
"""

from direct.showbase.ShowBase import ShowBase
from tools.envedit.camera_controller import CameraController
from tools.envedit.component_viewer import ComponentViewer
from tools.envedit.edenv_component import EComponent
from tools.envedit.floor_node import FloorNode
from tools.envedit.graph_node import GraphNode
from tools.envedit.graph_viewer import GraphViewer
from tools.envedit.envedit_data import EnveditData
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_font_loader import GUIFontLoader
from tools.envedit.gui.gui_system import GUISystem


class EnvEdit(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Initial scene setup
        self.disableMouse()
        self.setBackgroundColor(0.15, 0.15, 0.15, 1)

        # Set up GUI system
        self.gui_system = GUISystem(self)
        GUIFontLoader.base = self
        GUISystem.fonts["default"] = GUIFontLoader.load_font("open-sans/OpenSans-Regular.ttf")
        GUISystem.fonts["default_bold"] = GUIFontLoader.load_font("open-sans/OpenSans-Bold.ttf")
        GUISystem.fonts["default_light"] = GUIFontLoader.load_font("open-sans/OpenSans-Light.ttf")
        window_layout = GUIDockLayout()
        self.gui_system.window.set_child(window_layout)

        # Set up scene data
        self.envedit_data = EnveditData()
        self.envedit_data.update_callback = self.update_gui
        self.envedit_data.scene_root = GraphNode("Scene Root", [])

        # Add floor
        self.floor_node = FloorNode(self)
        floor_path = self.render.attach_new_node(self.floor_node)
        floor_path.setTwoSided(True)

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

        self.update_gui()

    # Updates the GUI after a change to the scene
    def update_gui(self):
        self.graph_viewer.update_viewer()
        self.component_viewer.update_viewer()

if __name__ == "__main__":
    app = EnvEdit()
    app.run()
