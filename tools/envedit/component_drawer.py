"""
A GUI component that displays properties of the EDEnv component.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_dropdown import GUIDropdownVisualType, GUIDropdown
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_menu_item import GUIMenuItem
from tools.envedit.gui.gui_number_box import GUINumberBox
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_text_box import GUITextBox
from tools.envedit.property_type import PropertyType


class ComponentDrawer(GUIFrame):

    def __init__(self, component=None):
        GUIFrame.__init__(self)
        self.component = component
        if self.component is not None:
            self.component.component_update_callback = self.component_change_handler
        self.envedit_data = None
        self.property_fields = {}

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
                property_layout.bbox.height = 30
                property_frame.set_child(property_layout)

                property_name = GUILabel()
                property_name.set_text(property + ":")
                property_layout.add_child(property_name)

                spacer = GUIComponent()
                spacer.bbox.width = 20
                property_layout.add_child(spacer)

                if property_type == PropertyType.INT:
                    property_val = GUINumberBox(use_int=True)
                    property_val.text_box.data = property
                    property_val.text_box.set_text(self.component.property_vals[property])
                    property_val.text_box.on_text_changed = self.text_change_handler
                    self.property_fields[property] = property_val
                    property_layout.add_child(property_val)
                elif property_type == PropertyType.FLOAT:
                    property_val = GUINumberBox()
                    property_val.text_box.data = property
                    property_val.text_box.set_text(self.component.property_vals[property])
                    property_val.text_box.on_text_changed = self.text_change_handler
                    self.property_fields[property] = property_val
                    property_layout.add_child(property_val)
                elif property_type == PropertyType.BOOL:
                    property_val = GUITextBox()
                    property_val.data = property
                    property_val.set_text(self.component.property_vals[property])
                    property_val.on_text_changed = self.text_change_handler
                    self.property_fields[property] = property_val
                    property_layout.add_child(property_val)
                elif property_type == PropertyType.STRING:
                    property_val = GUITextBox()
                    property_val.data = property
                    property_val.set_text(self.component.property_vals[property])
                    property_val.on_text_changed = self.text_change_handler
                    self.property_fields[property] = property_val
                    property_layout.add_child(property_val)
                elif property_type == PropertyType.FILE:
                    property_val = GUITextBox()
                    property_val.data = property
                    property_val.set_text(self.component.property_vals[property])
                    property_val.on_text_changed = self.text_change_handler
                    self.property_fields[property] = property_val
                    property_layout.add_child(property_val)
                elif property_type == PropertyType.ARRAY:
                    property_val = GUIStackLayout()
                    property_val.bbox.width = 124

                    add_button = GUIButton()
                    add_button.padding = 2
                    add_button.bbox.width = 20
                    add_button.bbox.height = 20
                    add_button.data = property
                    add_button.on_click = self.add_button_handler
                    button_label = GUILabel()
                    button_label.receive_events = False
                    button_label.set_text("Add Element")
                    add_button.set_child(button_label)
                    property_val.add_child(add_button)

                    vals = self.component.property_vals[property]
                    for i in range(len(vals)):
                        val = vals[i]

                        element_layout = GUIStackLayout(vertical=False)
                        element_layout.padding = 4
                        element_layout.bbox.height = 28
                        property_val.add_child(element_layout)

                        inner_property_val = GUITextBox()
                        inner_property_val.data = {"parent": property, "index": i}
                        inner_property_val.set_text(val)
                        inner_property_val.on_text_changed = self.text_change_handler
                        element_layout.add_child(inner_property_val)

                        element_spacer = GUIComponent()
                        element_spacer.bbox.width = 4
                        element_layout.add_child(element_spacer)

                        del_button = GUIButton()
                        del_button.padding = 3
                        del_button.bbox.width = 16
                        del_button.bbox.height = 20
                        del_button.set_normal_color((1, 0, 0, 0.8))
                        del_button.set_hover_color((1, 0.4, 0.4, 0.8))
                        del_button.set_pressed_color((0.4, 0, 0, 0.8))
                        del_button.on_click = self.element_del_button_handler
                        del_button.data = element_layout
                        del_button_label = GUILabel()
                        del_button_label.set_text("X")
                        del_button_label.receive_events = False
                        del_button.set_child(del_button_label)
                        element_layout.add_child(del_button)

                    self.property_fields[property] = property_val
                    property_layout.add_child(property_val)
                    property_frame.fit_height_to_content = True
                    property_layout.bbox.height = property_val.bbox.height

    def del_option_handler(self, item):
        self.envedit_data.target_node.remove_component(item.data)
        self.envedit_data.modify()
        self.envedit_data.update()

    def set_envedit_data(self, data):
        self.envedit_data = data

    # Handles the text change
    def text_change_handler(self, text_box):
        if isinstance(text_box.data, dict):
            self.component.property_vals[text_box.data["parent"]][text_box.data["index"]] = text_box.text
        else:
            self.component.property_vals[text_box.data] = text_box.text
        self.component.node.component_property_changed_selected()
        self.envedit_data.modify()
        self.envedit_data.update()

    # Handles the add button for array component drawer
    def add_button_handler(self, button):
        # Add new element to array
        self.component.property_vals[button.data].append("")

        # Add new field to list of elements
        element_layout = GUIStackLayout(vertical=False)
        element_layout.padding = 4
        element_layout.bbox.height = 28
        self.property_fields[button.data].add_child(element_layout)

        inner_property_val = GUITextBox()
        inner_property_val.data = {"parent": button.data, "index": len(self.component.property_vals[button.data]) - 1}
        inner_property_val.set_text("")
        inner_property_val.on_text_changed = self.text_change_handler
        element_layout.add_child(inner_property_val)

        element_spacer = GUIComponent()
        element_spacer.bbox.width = 4
        element_layout.add_child(element_spacer)

        del_button = GUIButton()
        del_button.padding = 3
        del_button.bbox.width = 16
        del_button.bbox.height = 20
        del_button.set_normal_color((1, 0, 0, 0.8))
        del_button.set_hover_color((1, 0.4, 0.4, 0.8))
        del_button.set_pressed_color((0.4, 0, 0, 0.8))
        del_button.on_click = self.element_del_button_handler
        del_button.data = element_layout
        del_button_label = GUILabel()
        del_button_label.set_text("X")
        del_button_label.receive_events = False
        del_button.set_child(del_button_label)
        element_layout.add_child(del_button)

    # Handles the delete button for array component drawer
    def element_del_button_handler(self, button):
        property_name = button.data.children[0].data["parent"]
        element_index = button.data.children[0].data["index"]

        # Remove element from array
        self.component.property_vals[property_name].pop(element_index)

        # Remove element from list of elements
        self.property_fields[property_name].remove_child(button.data)

        # Reset the element indices
        for i in range(len(self.property_fields[property_name].children)):
            element = self.property_fields[property_name].children[i]
            if isinstance(element, GUIStackLayout):
                element.children[0].data["parent"] = property_name
                element.children[0].data["index"] = i - 1

    # Handles component changing values
    def component_change_handler(self, property_name):
        property_type = self.component.property_types[property_name]
        property_val = self.property_fields[property_name]

        if property_type == PropertyType.INT:
            property_val.text_box.set_text(self.component.property_vals[property_name])
        elif property_type == PropertyType.FLOAT:
            property_val.text_box.set_text(str(int(float(self.component.property_vals[property_name]) * 1000) / 1000))
        elif property_type == PropertyType.BOOL:
            property_val.set_text(self.component.property_vals[property_name])
        elif property_type == PropertyType.STRING:
            property_val.set_text(self.component.property_vals[property_name])
        elif property_type == PropertyType.FILE:
            property_val.set_text(self.component.property_vals[property_name])
        elif property_type == PropertyType.ARRAY:
            property_val.set_text(self.component.property_vals[property_name])
