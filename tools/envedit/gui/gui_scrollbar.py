"""
Scrollbar for the GUI system.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_button import GUIButton
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_system import GUISystem


class GUIScrollbar(GUIFrame):

    def __init__(self, vertical=True):
        GUIFrame.__init__(self)
        self.set_bg_color((1, 1, 1, 0.1))
        self.start_pos = 0
        self.start_offset = 0
        self.offset = 0
        self.on_scroll = None
        self.scroll_size = 40
        self.vertical = vertical

        self.scroll_button = GUIButton()
        if self.vertical:
            self.bbox.width = 10
            self.scroll_button.bbox.width = 10
            self.scroll_button.bbox.height = self.scroll_size
        else:
            self.bbox.height = 10
            self.scroll_button.bbox.width = self.scroll_size
            self.scroll_button.bbox.height = 10

        self.scroll_button.set_normal_color((1, 1, 1, 0.8))
        self.scroll_button.set_pressed_color(self.scroll_button.hover_color)
        self.scroll_button.on_click = self.scroll_button_pressed
        self.set_child(self.scroll_button)

    def update(self):
        GUIFrame.update(self)
        if self.child is not None:
            if self.vertical:
                self.scroll_button.bbox.width = 10
                self.scroll_button.bbox.height = self.scroll_size
                self.child.bbox.y = self.bbox.y + self.offset
            else:
                self.scroll_button.bbox.width = self.scroll_size
                self.scroll_button.bbox.height = 10
                self.child.bbox.x = self.bbox.x + self.offset
            self.child.set_clip_region(self.clip_region.get_intersection(self.bbox))
            self.child.update()

    def scroll_button_pressed(self, button):
        GUISystem.set_drag(self)
        if self.vertical:
            self.start_pos = GUISystem.gui_system.cursor_y
        else:
            self.start_pos = GUISystem.gui_system.cursor_x
        self.start_offset = self.offset

    def handle_drag(self, cursor_x, cursor_y):
        if self.vertical:
            self.offset = min(self.bbox.height - self.child.bbox.height, max(0, self.start_offset + cursor_y - self.start_pos))
        else:
            self.offset = min(self.bbox.width - self.child.bbox.width, max(0, self.start_offset + cursor_x - self.start_pos))
        self.update()

        if self.on_scroll is not None:
            self.on_scroll(self.offset)
