"""
Controls the component viewer.

@author Ben Giacalone
"""
from tools.envedit.component_drawer import ComponentDrawer
from tools.envedit.edenv_component import EComponent
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_dropdown import GUIDropdown
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_menu_item import GUIMenuItem
from tools.envedit.gui.gui_scroll_container import GUIScrollContainer
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

        master_layout = GUIDockLayout()
        self.set_child(master_layout)

        self.layout = GUIStackLayout()
        master_layout.set_child_dock(self.layout, GUIDockLayout.TOP)

        title = GUILabel()
        title.text_size = 30
        title.set_font(GUISystem.get_font("default_light"))
        title.set_text("Components")
        self.layout.add_child(title)

        spacer = GUIComponent()
        spacer.bbox.height = 20
        self.layout.add_child(spacer)

        self.add_component_dropdown = GUIDropdown()
        self.add_component_dropdown.child.set_text("Add Component...")

        scroll_container = GUIScrollContainer(scroll_v=True, scroll_h=True)
        master_layout.set_child_dock(scroll_container, GUIDockLayout.CENTER)

        self.component_layout = GUIStackLayout()
        scroll_container.set_child(self.component_layout)

    # Sets up the components for the viewer
    def setup_components(self):
        if self.envedit_data is not None and self.envedit_data.target_node is not None:
            # Remove drawers that don't exist
            remove_list = []
            for i in range(len(self.component_layout.children)):
                drawer = self.component_layout.children[i]
                if i >= len(self.envedit_data.target_node.data) or drawer.component is not self.envedit_data.target_node.data[i]:
                    remove_list.append(drawer)
            for drawer in remove_list:
                self.component_layout.remove_child(drawer)

            # Add new drawers
            for i in range(len(self.envedit_data.target_node.data)):
                component = self.envedit_data.target_node.data[i]
                if i >= len(self.component_layout.children) or component is not self.component_layout.children[i].component:
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
            # Only add "add component" button if scene root isn't selected
            self.layout.remove_child(self.add_component_dropdown)
            if self.envedit_data.target_node is not self.envedit_data.scene_root:
                self.layout.add_child(self.add_component_dropdown, 2)

            # Set up the node's components
            self.setup_components()
            self.update()

    # Sets the list of components from configuration file
    def set_components(self, components):
        self.add_component_dropdown.menu.child.clear()
        self.components = components
        # Add "add component" menu items
        for component in self.components:
            component_item = GUIMenuItem()
            component_item.child.set_text(EComponent.from_script(component).name)
            component_item.on_release = self.add_component_handler
            component_item.data = component
            self.add_component_dropdown.menu.child.add_child(component_item)

    # Handles a component to add being selected
    def add_component_handler(self, item):
        component = EComponent.from_script(item.data)
        self.envedit_data.target_node.add_component(component)
        self.envedit_data.target_node.component_property_changed_selected()
        self.envedit_data.modify()
        self.envedit_data.update()
