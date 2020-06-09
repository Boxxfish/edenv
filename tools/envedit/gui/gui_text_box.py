"""
A text box that accepts typed text.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_stack_layout import GUIStackLayout
from tools.envedit.gui.gui_system import GUISystem


class GUITextBox(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.cursor_pos = 0
        self.focused = False
        self.bbox.height = 20
        self.bbox.width = 100
        self.padding = 4
        self.text = ""
        self.normal_color = (1, 1, 1, 0.2)
        self.focus_color = (0.6, 0.6, 0.6, 0.2)
        self.normal_text_color = (1, 1, 1, 1)
        self.invalid_text_color = (1, 0, 0, 1)
        self.curr_text_color = self.normal_text_color
        self.set_bg_color(self.normal_color)

        self.use_single_label()

        self.on_text_changed = None     # Called when text is changed
        self.on_lost_focus = None       # Called when textbox loses focus
        self.validate_text = None       # Called to check if text is in correct format
        self.data = None

    def update(self):
        # This is more complicated than it should be... figure out why we can't just check for self.focused
        if self.focused and self.child is not None and len(self.child.children) > 0:
            # Set the text of both text boxes
            self.child.children[0].set_text(self.text[:self.cursor_pos])
            self.child.children[2].set_text(self.text[self.cursor_pos:])

        GUIFrame.update(self)

        if self.focused and self.child is not None and len(self.child.children) > 0:
            # Move the text boxes so the cursor is on the screen
            if self.bbox.x + self.bbox.width < self.child.children[2].bbox.x:
                self.child.bbox.x = self.bbox.x - (self.child.children[0].bbox.width - self.bbox.width) - 4
            self.child.set_clip_region(self.clip_region.get_intersection(self.bbox))
            self.child.update()


    # Sets the child element to a single text label
    def use_single_label(self):
        if self.child is not None:
            self.remove_child()
        self.set_child(GUILabel())
        self.child.set_text_color(self.curr_text_color)
        self.child.receive_events = False
        self.child.set_text(self.text)
        self.update()

    # Sets the child element to a stack of text labels (for rendering the cursor)
    def use_stacked_labels(self):
        if self.child is not None:
            self.remove_child()
        self.set_child(GUIStackLayout(vertical=False))
        self.child.bbox.height = self.bbox.height

        first_label = GUILabel()
        first_label.set_text_color(self.curr_text_color)
        first_label.receive_events = False
        self.child.add_child(first_label)

        cursor = GUIFrame()
        cursor.bbox.width = 1
        cursor.set_bg_color((1, 1, 1, 1))
        cursor.receive_events = False
        self.child.add_child(cursor)

        second_label = GUILabel()
        second_label.set_text_color(self.curr_text_color)
        second_label.receive_events = False
        self.child.add_child(second_label)

        self.update()

    def set_text(self, text):
        # Validate text
        self.text = text
        text_valid = True
        if self.validate_text is not None:
            text_valid = self.validate_text(text)

        # Set text
        if self.focused:
            self.child.children[0].set_text(self.text[:self.cursor_pos])
            self.child.children[2].set_text(self.text[self.cursor_pos:])
        else:
            self.child.set_text(self.text)

        if text_valid:
            self.curr_text_color = self.normal_text_color
            if self.on_text_changed is not None:
                self.on_text_changed(self)
        else:
            self.curr_text_color = self.invalid_text_color
        self.set_text_color(self.curr_text_color)
        self.update()

    def set_text_color(self, color):
        if self.focused:
            self.child.children[0].set_text_color(color)
            self.child.children[2].set_text_color(color)
        else:
            self.child.set_text_color(color)

    def handle_left_pressed(self):
        self.cursor_pos = len(self.text)
        self.focused = True
        self.use_stacked_labels()
        self.set_bg_color(self.focus_color)
        GUISystem.set_focus(self)

    def handle_lost_focus(self):
        self.focused = False
        self.use_single_label()
        self.set_bg_color(self.normal_color)
        if self.on_lost_focus is not None:
            self.on_lost_focus(self)

    def handle_keystroke(self, key):
        new_text = self.text[:self.cursor_pos] + key + self.text[self.cursor_pos:]
        self.cursor_pos += 1
        self.set_text(new_text)

    def handle_special_key(self, key):
        if key == "backspace":
            if self.cursor_pos != 0:
                self.set_text(self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:])
                self.cursor_pos -= 1
                self.update()
        elif key == "arrow_left":
            if self.cursor_pos != 0:
                self.cursor_pos -= 1
                self.update()
        elif key == "arrow_right":
            if self.cursor_pos != len(self.text):
                self.cursor_pos += 1
                self.update()
        elif key == "delete":
            if self.cursor_pos != len(self.text):
                self.set_text(self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:])
                self.update()
        elif key == "enter":
            GUISystem.release_focus()
