"""
Controls the component viewer.

@author Ben Giacalone
"""
from os import path
from pathlib import Path
from tools.envedit.component_drawer import ComponentDrawer
from tools.envedit.edenv_component import EComponent
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_system import GUISystem


class ComponentViewer(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)

        self.envedit_data = None

        # GUI settings
        self.bg_color = (0, 0, 0, 0.8)
        self.bbox.width = 300
        self.padding = 10

        layout = GUIStackLayout()
        self.set_child(layout)

        title = GUILabel()
        title.text_size = 30
        title.set_font(GUISystem.get_font("default_light"))
        title.set_text("Components")
        layout.add_child(title)

        spacer = GUIComponent()
        spacer.bbox.height = 20
        layout.add_child(spacer)

        self.component_layout = GUIStackLayout()
        layout.add_child(self.component_layout)

        self.setup_components()

    # Sets up the components for the viewer
    def setup_components(self):
        if self.envedit_data is not None and self.envedit_data.target_node is not None:
            for component in self.envedit_data.target_node.data:
                self.component_layout.add_child(ComponentDrawer(component))

    # Clears the component viewer
    def clear_viewer(self):
        for child in self.component_layout.children:
            self.component_layout.remove_child(child)

    # Sets the data model
    def set_envedit_data(self, envedit_data):
        self.envedit_data = envedit_data

    # Updates the viewer
    def update_viewer(self):
        if self.envedit_data is not None and self.envedit_data.target_node is not None:
            self.clear_viewer()
            self.setup_components()
            self.update()
