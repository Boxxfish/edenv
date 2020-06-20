"""
Envedit's toolbar.

@author Ben Giacalone
"""
import subprocess
from pathlib import Path

from panda3d.core import NodePath

from tools.envedit.envedit_data import EnveditData
from tools.envedit.graph_node import GraphNode
from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
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
        self.bbox.height = 64
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

        open_button = GUIMenuItem()
        open_button.child.set_text("Open...")
        open_button.on_release = self.file_open_option_handler
        file_dropdown.menu.child.add_child(open_button)

        save_button = GUIMenuItem()
        save_button.child.set_text("Save")
        save_button.on_release = self.file_save_option_handler
        file_dropdown.menu.child.add_child(save_button)

        save_as_button = GUIMenuItem()
        save_as_button.child.set_text("Save As...")
        save_as_button.on_release = self.file_save_as_option_handler
        file_dropdown.menu.child.add_child(save_as_button)

        buttons_layout.add_child(file_dropdown)

        edit_dropdown = GUIDropdown()
        edit_dropdown.child.text_size = 15
        edit_dropdown.child.set_text("Edit")
        edit_dropdown.fit_width_to_content = True
        edit_dropdown.padding = 6
        buttons_layout.add_child(edit_dropdown)

        middle_border = GUIFrame()
        middle_border.set_bg_color((0.2, 0.2, 0.2, 1))
        middle_border.bbox.height = 1
        self.child.add_child(middle_border)

        bottom_bar_layout = GUIDockLayout()
        bottom_bar_layout.bbox.height = 28
        self.child.add_child(bottom_bar_layout)

        icons_layout = GUIStackLayout(vertical=False)
        bottom_bar_layout.set_child_dock(icons_layout, GUIDockLayout.LEFT)

        translate_button = GUIButton()
        translate_button.bbox.width = 30
        translate_button.bbox.height = 30
        translate_button.set_normal_color((1, 1, 1, 0.9))
        translate_button.set_pressed_color((0, 0, 0, 0.9))
        translate_button.set_bg_image("translate_icon.png")
        translate_button.on_click = self.translate_button_handler
        icons_layout.add_child(translate_button)

        rotate_button = GUIButton()
        rotate_button.bbox.width = 30
        rotate_button.bbox.height = 30
        rotate_button.set_normal_color((1, 1, 1, 0.9))
        rotate_button.set_pressed_color((0, 0, 0, 0.9))
        rotate_button.set_bg_image("rotate_icon.png")
        rotate_button.on_click = self.rotate_button_handler
        icons_layout.add_child(rotate_button)

        scale_button = GUIButton()
        scale_button.bbox.width = 30
        scale_button.bbox.height = 30
        scale_button.set_normal_color((1, 1, 1, 0.9))
        scale_button.set_pressed_color((0, 0, 0, 0.9))
        scale_button.set_bg_image("scale_icon.png")
        scale_button.on_click = self.scale_button_handler
        icons_layout.add_child(scale_button)

        play_layout = GUIStackLayout(vertical=False)
        bottom_bar_layout.set_child_dock(play_layout, GUIDockLayout.RIGHT)

        play_button = GUIButton()
        play_button.bbox.width = 30
        play_button.bbox.height = 30
        play_button.set_normal_color((0.2, 0.8, 0.2, 0.9))
        play_button.set_hover_color((0.2, 0.9, 0.2, 0.9))
        play_button.set_pressed_color((0.2, 0.5, 0.2, 0.9))
        play_button.set_bg_image("play_icon.png")
        play_button.on_click = self.play_button_handler
        play_layout.add_child(play_button)

        play_spacer = GUIComponent()
        play_spacer.bbox.width = 150
        play_layout.add_child(play_spacer)

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
            if file_path != "":
                self.envedit_data.save(file_path)
        else:
            self.envedit_data.save()

    def file_save_as_option_handler(self, item):
        # Open file dialog
        filetypes = [("JSON", "*.json")]
        file_path = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes)

        # Save file
        if file_path != "":
            self.envedit_data.save(file_path)

    def file_open_option_handler(self, item):
        # Open file dialog
        filetypes = [("JSON", "*.json")]
        file_path = filedialog.askopenfilename(filetypes=filetypes, defaultextension=filetypes)

        # Load file
        if file_path != "":
            for child in self.envedit_data.panda_root_node.children:
                NodePath(child).removeNode()
            self.envedit_data.load(file_path)

        # TODO: When scene data is loaded, if the dirt flag is set, bring up save dialog

    def translate_button_handler(self, button):
        self.envedit_data.set_transform_gizmo(EnveditData.TRANSLATE_GIZMO)

    def rotate_button_handler(self, button):
        self.envedit_data.set_transform_gizmo(EnveditData.ROTATE_GIZMO)

    def scale_button_handler(self, button):
        self.envedit_data.set_transform_gizmo(EnveditData.SCALE_GIZMO)

    def play_button_handler(self, button):
        run_path = Path(__file__).parent.parent / "run/run.py"
        if self.envedit_data.save_path is not None:
            subprocess.call(["python", str(run_path), "-e", self.envedit_data.save_path[:-5], "-t", "1", "-v", "1"])
