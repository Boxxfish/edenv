"""
Controls the component viewer.

@author Ben Giacalone
"""
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

        # List of components
        self.components = []
        self.components.append(EComponent("Position"))
        self.components.append(EComponent("MeshGraphic"))

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
        for component in self.components:
            self.component_layout.add_child(ComponentDrawer(component))
