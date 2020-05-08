"""
EDEnv's GUI manager.

@author Ben Giacalone
"""
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

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

        # Update GUIUtils
        GUIUtils.window_width = self.base.win.getXSize()
        GUIUtils.window_height = self.base.win.getYSize()

        # Set up GUI components
        self.window = GUIWindow()
        self.window.rendering = True
        self.target_component = self.window     # the target is the component the cursor is currently over

        # Set up mouse polling
        self.cursor_x = 0
        self.cursor_y = 0
        self.addTask(self.poll_cursor)

    # Window event handler
    def handle_window(self, window):
        GUIUtils.window_width = window.size.x
        GUIUtils.window_height = window.size.y
        self.window.window_resized(window.size.x, window.size.y)

    # Left mouse pressed event handler
    def handle_left_mouse_pressed(self):
        if self.target_component is not None:
            self.target_component.handle_left_pressed()

    # Left mouse released event handler
    def handle_left_mouse_released(self):
        if self.target_component is not None:
            self.target_component.handle_left_released()

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
        GUISystem.gui_system.window.update()