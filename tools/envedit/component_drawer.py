"""
A GUI component that displays properties of the EDEnv component.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_dropdown import GUIDropdownVisualType, GUIDropdown
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_menu_item import GUIMenuItem
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_text_box import GUITextBox


class ComponentDrawer(GUIFrame):

    def __init__(self, component=None):
        GUIFrame.__init__(self)
        self.component = component
        self.envedit_data = None

        # GUI settings
        self.fit_height_to_content = True
        self.padding = 10
        self.set_bg_color((1, 1, 1, 0.2))

        layout = GUIStackLayout()
        self.set_child(layout)

        title_layout = GUIDockLayout()
        title_layout.bbox.height = 30
        layout.add_child(title_layout)

        self.title = GUILabel()
        self.title.text_size = 15
        self.title.set_text(self.component.name)
        title_layout.set_child_dock(self.title, GUIDockLayout.LEFT)

        options_dropdown = GUIDropdown(GUIDropdownVisualType.VERTICAL)
        title_layout.set_child_dock(options_dropdown, GUIDockLayout.RIGHT)

        del_option = GUIMenuItem()
        del_option.child.set_text("Delete Component")
        del_option.data = self.component
        del_option.on_release = self.del_option_handler
        options_dropdown.menu.child.add_child(del_option)

        self.properties_layout = GUIStackLayout()
        layout.add_child(self.properties_layout)

        self.setup_drawer()

    # Sets up the component drawer
    def setup_drawer(self):
        if self.component is not None:
            for property in self.component.property_types:
                property_type = self.component.property_types[property]

                property_frame = GUIFrame()
                property_frame.bbox.height = 30
                property_frame.padding = 4
                self.properties_layout.add_child(property_frame)

                property_layout = GUIStackLayout(vertical=False)
                property_frame.set_child(property_layout)

                property_name = GUILabel()
                property_name.set_text(property + ":")
                property_layout.add_child(property_name)

                spacer = GUIComponent()
                spacer.bbox.width = 20
                property_layout.add_child(spacer)

                property_val = GUITextBox()
                property_val.data = property
                property_val.set_text(self.component.property_vals[property])
                property_val.on_text_changed = self.text_change_handler
                property_layout.add_child(property_val)

    def del_option_handler(self, item):
        self.envedit_data.target_node.data.remove(item.data)
        self.envedit_data.modify()
        self.envedit_data.update()

    def set_envedit_data(self, data):
        self.envedit_data = data

    # Handles the text change
    def text_change_handler(self, text_box):
        self.component.property_vals[text_box.data] = text_box.text
        self.component.property_changed()
        self.envedit_data.modify()
        self.envedit_data.update()
