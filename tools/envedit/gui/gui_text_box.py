"""
A text box that accepts typed text.

@author Ben Giacalone
"""
from direct.gui.DirectEntry import DirectEntry

from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_system import GUISystem
from tools.envedit.gui.panda_gui_utils import GUIUtils


class GUITextBox(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.text = ""
        self.font = GUISystem.get_font("default")
        self.text_color = (1, 1, 1, 1)
        self.bg_color = (1, 1, 1, 0.2)
        self.text_size = 12
        self.frame = None
        self.on_text_changed = None
        self.data = None

    def set_text(self, text):
        self.text = text

    def update(self):
        if self.rendering:
            self.frame.initialText = self.text
            self.frame["text_fg"] = self.text_color
            self.frame["frameColor"] = self.bg_color
            self.frame.entryFont = self.font
            bounds = self.frame.getBounds()
            scale = (self.text_size * 2.5) / (GUIUtils.square_size + 1)
            self.bbox.width, self.bbox.height = GUIUtils.get_screen_space_size((bounds[1] - bounds[0]) * scale,
                                                                               (bounds[3] - bounds[2]) * scale)
            x, y, width, height = GUIUtils.get_panda_text_coords(self.bbox.x, self.bbox.y, self.bbox.width,
                                                                 self.bbox.height)
            self.frame.setPos(x, 0, y)
            self.frame.setScale(scale)

    def add_render(self):
        self.rendering = True
        self.frame = DirectEntry(initialText=self.text,
                                 text_fg=self.text_color,
                                 frameColor=self.bg_color,
                                 text_font=self.font,
                                 focusOutCommand=self.focus_out_handler,
                                 scale=(self.text_size * 2.5) / (GUIUtils.square_size + 1))
        if self.child is not None:
            self.child.add_render()
        self.update()

    def stop_render(self):
        if self.rendering:
            self.frame.destroy()
            self.frame = None
        self.rendering = False
        if self.child is not None:
            self.child.stop_render()
        self.update()

    # Handles focus exit
    def focus_out_handler(self):
        should_trigger = self.text != self.frame.get()
        self.text = self.frame.get()
        if should_trigger and self.on_text_changed is not None:
            self.on_text_changed(self)
