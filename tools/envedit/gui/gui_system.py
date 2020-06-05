"""
EDEnv's GUI manager.

@author Ben Giacalone
"""
import string

from direct.showbase.DirectObject import DirectObject
from direct.task import Task

from tools.envedit.gui.bounding_box import BoundingBox
from tools.envedit.gui.gui_context_menu import GUIContextMenu
from tools.envedit.gui.panda_gui_utils import GUIUtils
from tools.envedit.gui.gui_window import GUIWindow


class GUISystem(DirectObject):
    fonts = {}
    gui_system = None

    def __init__(self, base):
        DirectObject.__init__(self)
        self.base = base
        GUISystem.gui_system = self

        # Register events
        self.accept("window-event", self.handle_window)
        self.accept("mouse1", self.handle_left_mouse_pressed)
        self.accept("mouse1-up", self.handle_left_mouse_released)
        self.accept("mouse3", self.handle_right_mouse_pressed)
        self.accept("mouse3-up", self.handle_right_mouse_released)
        self.base.buttonThrowers[0].node().setKeystrokeEvent("keystroke")
        self.accept("keystroke", self.handle_keystroke)
        self.accept("backspace", self.handle_backspace)
        self.accept("backspace-repeat", self.handle_backspace)
        self.accept("arrow_left", self.handle_arrow_left)
        self.accept("arrow_left-repeat", self.handle_arrow_left)
        self.accept("arrow_right", self.handle_arrow_right)
        self.accept("arrow_right-repeat", self.handle_arrow_right)
        self.accept("delete", self.handle_delete)
        self.accept("delete-repeat", self.handle_delete)
        self.accept("enter", self.handle_enter)

        # Update GUIUtils
        GUIUtils.window_width = self.base.win.getXSize()
        GUIUtils.window_height = self.base.win.getYSize()

        # Set up GUI components
        self.window = GUIWindow()
        self.window.add_render()
        self.target_component = self.window     # the target is the component the cursor is currently over
        self.focus_component = self.window      # the focus component is the component that's currently focused

        # Set up mouse polling
        self.cursor_x = 0
        self.cursor_y = 0
        self.addTask(self.poll_cursor)

    # Window event handler
    def handle_window(self, window):
        GUIUtils.window_width = window.size.x
        GUIUtils.window_height = window.size.y
        self.window.window_resized(window.size.x, window.size.y)
        GUISystem.close_context_menu()

    # Left mouse pressed event handler
    def handle_left_mouse_pressed(self):
        if not self.window.selected_context_menu:
            GUISystem.close_context_menu()
        if self.target_component is not None:
            self.target_component.handle_left_pressed()

        # Force system to reset target component on next loop
        self.cursor_x = -1
        self.cursor_y = -1

    # Left mouse released event handler
    def handle_left_mouse_released(self):
        if self.target_component is not None:
            self.target_component.handle_left_released()

        # Force system to reset target component on next loop
        self.cursor_x = -1
        self.cursor_y = -1

    # Right mouse pressed event handler
    def handle_right_mouse_pressed(self):
        if not self.window.selected_context_menu:
            GUISystem.close_context_menu()
        if self.target_component is not None:
            self.target_component.handle_right_pressed()

        # Force system to reset target component on next loop
        self.cursor_x = -1
        self.cursor_y = -1

    # Right mouse released event handler
    def handle_right_mouse_released(self):
        if self.target_component is not None:
            self.target_component.handle_right_released()

        # Force system to reset target component on next loop
        self.cursor_x = -1
        self.cursor_y = -1

    # Keystroke event handler
    def handle_keystroke(self, key):
        if self.focus_component is not None and key in (string.ascii_letters + string.digits + string.punctuation + " "):
            self.focus_component.handle_keystroke(key)

    # Backspace event handler
    def handle_backspace(self):
        if self.focus_component is not None:
            self.focus_component.handle_special_key("backspace")

    # Left arrow key event handler
    def handle_arrow_left(self):
        if self.focus_component is not None:
            self.focus_component.handle_special_key("arrow_left")

    # Right arrow key event handler
    def handle_arrow_right(self):
        if self.focus_component is not None:
            self.focus_component.handle_special_key("arrow_right")

    # Delete key event handler
    def handle_delete(self):
        if self.focus_component is not None:
            self.focus_component.handle_special_key("delete")

    # Enter key event handler
    def handle_enter(self):
        if self.focus_component is not None:
            self.focus_component.handle_special_key("enter")

    # Cursor position polling task
    def poll_cursor(self, task):
        if self.base.mouseWatcherNode.hasMouse():
            # Get new cursor coordinates in screen space
            new_x = self.base.win.getXSize() * ((self.base.mouseWatcherNode.getMouseX() + 1) / 2)
            new_y = self.base.win.getYSize() * (1 - (self.base.mouseWatcherNode.getMouseY() + 1) / 2)

            # If the position's changed, change target and trigger cursor events for old and new target
            if new_x != self.cursor_x or new_y != self.cursor_y:
                old_target = self.target_component
                self.target_component = self.window.get_selected_component(new_x, new_y)
                if old_target != self.target_component:
                    if self.target_component is not None:
                        self.target_component.handle_cursor_enter()
                    if old_target is not None:
                        old_target.handle_cursor_exit()
                self.cursor_x = new_x
                self.cursor_y = new_y
        return Task.cont

    # Retrieves the font specified
    @staticmethod
    def get_font(font_name):
        if font_name in GUISystem.fonts:
            return GUISystem.fonts[font_name]

    # Updates the entire UI
    # This should NEVER be called from a component's update
    @staticmethod
    def update_all():
        GUISystem.gui_system.window.update(BoundingBox())

    # Creates a context menu at the current cursor location
    # Returns a component
    @staticmethod
    def create_context_menu():
        context_menu = GUIContextMenu()
        context_menu.bbox.x = GUISystem.gui_system.cursor_x
        context_menu.bbox.y = GUISystem.gui_system.cursor_y
        GUISystem.gui_system.window.context_menu_layer.add_child(context_menu)
        return context_menu

    # Places a context menu below a component
    # Returns a component
    @staticmethod
    def place_dropdown(parent, menu):
        menu.bbox.x = parent.bbox.x
        menu.bbox.y = parent.bbox.y + parent.bbox.height
        GUISystem.gui_system.window.context_menu_layer.add_child(menu)

    # Closes any context menus
    @staticmethod
    def close_context_menu():
        GUISystem.gui_system.window.context_menu_layer.clear()

    # Sets the current focused component
    @staticmethod
    def set_focus(component):
        if GUISystem.gui_system.focus_component is not component:
            GUISystem.gui_system.focus_component.handle_lost_focus()
        GUISystem.gui_system.focus_component = component

    # Sets the current focused component to the window
    @staticmethod
    def release_focus():
        GUISystem.set_focus(GUISystem.gui_system.window)
