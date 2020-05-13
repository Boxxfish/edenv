"""
Controls the component viewer.

@author Ben Giacalone
"""
from tools.envedit.component_drawer import ComponentDrawer
from tools.envedit.edenv_component import EComponent
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_dropdown import GUIDropdown
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_menu_item import GUIMenuItem
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_system import GUISystem


class ComponentViewer(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.components = None
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

        self.add_component_dropdown = GUIDropdown()
        self.add_component_dropdown.child.set_text("Add Component...")
        layout.add_child(self.add_component_dropdown)

        self.component_layout = GUIStackLayout()
        layout.add_child(self.component_layout)

    # Sets up the components for the viewer
    def setup_components(self):
        if self.envedit_data is not None and self.envedit_data.target_node is not None:
            for component in self.envedit_data.target_node.data:
                drawer = ComponentDrawer(component)
                drawer.set_envedit_data(self.envedit_data)
                self.component_layout.add_child(drawer)

    # Clears the component viewer
    def clear_viewer(self):
        self.component_layout.clear()

    # Sets the data model
    def set_envedit_data(self, envedit_data):
        self.envedit_data = envedit_data

    # Updates the viewer
    def update_viewer(self):
        if self.envedit_data is not None and self.envedit_data.target_node is not None:
            self.clear_viewer()
            self.setup_components()
            self.update()

    # Sets the list of components from configuration file
    def set_components(self, components):
        self.components = components
        # Add "add component" menu items
        for component in self.components:
            component_item = GUIMenuItem()
            component_item.child.set_text(component)
            component_item.on_release = self.add_component_handler
            component_item.data = self.components[component]
            self.add_component_dropdown.menu.child.add_child(component_item)

    # Handles a component to add being selected
    def add_component_handler(self, item):
        component = EComponent()
        component.set_script(item.data)
        self.envedit_data.target_node.data.append(component)
        self.envedit_data.update()