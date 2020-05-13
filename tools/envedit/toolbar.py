"""
Envedit's toolbar.

@author Ben Giacalone
"""
from tools.envedit.graph_node import GraphNode
from tools.envedit.gui.gui_dropdown import GUIDropdown
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_menu_item import GUIMenuItem
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tkinter import filedialog


class Toolbar(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.envedit_data = None

        # GUI settings
        self.bbox.height = 34
        self.set_bg_color((0, 0, 0, 0.8))

        self.set_child(GUIStackLayout())

        buttons_layout = GUIStackLayout(vertical=False)
        buttons_layout.bbox.height = 34
        self.child.add_child(buttons_layout)

        file_dropdown = GUIDropdown()
        file_dropdown.child.text_size = 15
        file_dropdown.child.set_text("File")
        file_dropdown.fit_width_to_content = True
        file_dropdown.padding = 6

        new_button = GUIMenuItem()
        new_button.child.set_text("New")
        new_button.on_release = self.file_new_option_handler
        file_dropdown.menu.child.add_child(new_button)

        save_button = GUIMenuItem()
        save_button.child.set_text("Save")
        save_button.on_release = self.file_save_option_handler
        file_dropdown.menu.child.add_child(save_button)

        open_button = GUIMenuItem()
        open_button.child.set_text("Open")
        open_button.on_release = self.file_open_option_handler
        file_dropdown.menu.child.add_child(open_button)

        buttons_layout.add_child(file_dropdown)

        edit_dropdown = GUIDropdown()
        edit_dropdown.child.text_size = 15
        edit_dropdown.child.set_text("Edit")
        edit_dropdown.fit_width_to_content = True
        edit_dropdown.padding = 6
        buttons_layout.add_child(edit_dropdown)

        bottom_border = GUIFrame()
        bottom_border.set_bg_color((0.2, 0.2, 0.2, 1))
        bottom_border.bbox.height = 2
        self.child.add_child(bottom_border)

    def set_envedit_data(self, envedit_data):
        self.envedit_data = envedit_data

    def file_new_option_handler(self, item):
        # Reset the scene root
        self.envedit_data.scene_root.clear()
        self.envedit_data.update()

        # TODO: When scene data is reset, if the dirt flag is set, bring up save dialog

    def file_save_option_handler(self, item):
        if self.envedit_data.save_path is None:
            # Open file dialog
            filetypes = [("JSON", "*.json")]
            file_path = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes)

            # Save file
            if file_path is not "":
                self.envedit_data.save(file_path)
        else:
            self.envedit_data.save()

    def file_open_option_handler(self, item):
        # Open file dialog
        filetypes = [("JSON", "*.json")]
        file_path = filedialog.askopenfilename(filetypes=filetypes, defaultextension=filetypes)

        # Load file
        if file_path is not "":
            self.envedit_data.load(file_path)

        # TODO: When scene data is loaded, if the dirt flag is set, bring up save dialog
