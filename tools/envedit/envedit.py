"""
Environment editor for EDEnv.

@author Ben Giacalone
"""

from direct.showbase.ShowBase import ShowBase
from tools.envedit.camera_controller import CameraController
from tools.envedit.floor_node import FloorNode
from tools.envedit.graph_viewer import GraphViewer
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_font_loader import GUIFontLoader
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_list import GUIList
from tools.envedit.gui.gui_list_dropdown import GUIListDropdown
from tools.envedit.gui.gui_list_item import GUIListItem
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_system import GUISystem
from string import ascii_lowercase


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

        # Add floor
        self.floor_node = FloorNode(self)
        floor_path = self.render.attach_new_node(self.floor_node)
        floor_path.setTwoSided(True)

        # Add camera controller
        self.cam_controller = CameraController(self, self.render, self.camera)

        # Add graph viewer
        # self.graph_viewer = GraphViewer(self, self.render)

        test_frame3 = GUIFrame()
        test_frame3.bg_color = (0, 0, 0, 0.8)
        test_frame3.bbox.width = 300

        left_layout = GUIList()
        test_frame3.set_child(left_layout)

        for i in range(10):
            dropdown_item = GUIListDropdown(f"Item {i + 1}")
            for j in range(3):
                dropdown_item.add_sub_item(GUIListDropdown(f"Item {ascii_lowercase[j]}"))
            left_layout.add_item(dropdown_item)

        test_layout = GUIDockLayout()
        test_layout.set_child_dock(test_frame3, GUIDockLayout.RIGHT)

        self.gui_system.window.set_child(test_layout)


if __name__ == "__main__":
    app = EnvEdit()
    app.run()
