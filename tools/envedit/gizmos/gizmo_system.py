"""
Generates and manages gizmos.

@author Ben Giacalone
"""
from os import path
from pathlib import Path
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import Shader, Filename, NodePath, PNMImage


class GizmoSystem(DirectObject):
    gizmos = [None for _ in range(256)]
    gizmo_system = None

    def __init__(self, base, envedit_data):
        self.base = base
        self.envedit_data = envedit_data
        self.target_gizmo = None
        self.focus_gizmo = None
        self.drag_gizmo = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.raw_mouse_x = 0
        self.raw_mouse_y = 0
        GizmoSystem.gizmo_system = self

        # Create frame buffer
        self.frame_buffer = self.base.win.makeTextureBuffer("Color Picker Buffer",
                                                            self.base.win.getXSize(),
                                                            self.base.win.getYSize(),
                                                            to_ram=True)
        self.frame_buffer.setSort(-100)
        self.frame_buffer.setClearColor((0, 0, 0, 1))

        # Load object selection shader
        shader_folder_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/shaders"
        self.color_picker_shader = Shader.load(Shader.SL_GLSL,
                                               vertex=Filename(shader_folder_path / "picker.vert").cStr(),
                                               fragment=Filename(shader_folder_path / "picker.frag").cStr())

        # Set up color picking camera
        self.color_cam = self.base.makeCamera(self.frame_buffer)
        color_cam_options = NodePath("color_cam_options")
        color_cam_options.setShader(self.color_picker_shader)
        self.color_cam.node().setInitialState(color_cam_options.getState())

        # Register events
        self.accept("window-event", self.handle_window)
        self.accept("mouse1", self.handle_left_mouse_pressed)
        self.accept("mouse1-up", self.handle_left_mouse_released)
        self.accept("mouse3", self.handle_right_mouse_pressed)
        self.accept("mouse3-up", self.handle_right_mouse_released)

        # DEBUG: View color picking framebuffer
        # self.accept("v", self.base.bufferViewer.toggleEnable)

        # Remove background from selection
        GizmoSystem.gizmos[0] = 1

        # Add object selection task
        self.add_task(self.handle_object_selection)

    # Task to handle object selection
    def handle_object_selection(self, task):
        if self.base.mouseWatcherNode.hasMouse():
            # Get mouse screen space coords
            self.raw_mouse_x = self.base.mouseWatcherNode.getMouseX()
            self.raw_mouse_y = self.base.mouseWatcherNode.getMouseY()
            mouse_x = int(self.base.win.getXSize() * ((self.raw_mouse_x + 1) / 2))
            mouse_y = int(self.base.win.getYSize() * (1 - (self.raw_mouse_y + 1) / 2))

            if mouse_x != self.mouse_x or mouse_y != self.mouse_y:
                self.mouse_x = mouse_x
                self.mouse_y = mouse_y

                # Extract texture
                frame_texture = self.frame_buffer.getTexture()
                frame_pnm = PNMImage()
                frame_texture.store(frame_pnm)

                # Get object ID
                if 0 < self.mouse_x < self.base.win.getXSize() and 0 < self.mouse_y < self.base.win.getYSize():
                    object_id = frame_pnm.getPixel(self.mouse_x, self.mouse_y)[0]

                    # Change target gizmo
                    old_target = self.target_gizmo
                    self.target_gizmo = None if object_id == 0 else GizmoSystem.gizmos[object_id]

                    # Handle dragging element
                    if self.drag_gizmo is not None:
                        self.drag_gizmo.handle_drag()

                    # Call cursor enter and exit callbacks
                    if old_target != self.target_gizmo:
                        if self.target_gizmo is not None:
                            self.target_gizmo.handle_cursor_enter()
                        if old_target is not None:
                            old_target.handle_cursor_exit()

        return Task.cont

    # Handles window being resized
    def handle_window(self, window):
        # Regenerate frame buffer
        self.base.graphicsEngine.removeWindow(self.frame_buffer)
        self.frame_buffer = self.base.win.makeTextureBuffer("Color Picker Buffer", window.size.x, window.size.y, to_ram=True)
        self.frame_buffer.setSort(-100)
        self.frame_buffer.setClearColor((0, 0, 0, 1))

        # Set up color picking camera
        self.color_cam.removeNode()
        self.color_cam = self.base.makeCamera(self.frame_buffer)
        color_cam_options = NodePath("color_cam_options")
        color_cam_options.setShader(self.color_picker_shader)
        self.color_cam.node().setInitialState(color_cam_options.getState())

    # Handles left mouse button pressed
    def handle_left_mouse_pressed(self):
        if self.target_gizmo is not None:
            self.target_gizmo.handle_left_pressed()

        # Force system to reset target component on next loop
        self.mouse_x = -1
        self.mouse_y = -1

    # Handles left mouse button released
    def handle_left_mouse_released(self):
        GizmoSystem.release_drag()
        if self.target_gizmo is not None:
            self.target_gizmo.handle_left_released()

        # Force system to reset target component on next loop
        self.mouse_x = -1
        self.mouse_y = -1

    # Handles right mouse button pressed
    def handle_right_mouse_pressed(self):
        if self.target_gizmo is not None:
            self.target_gizmo.handle_right_pressed()

        # Force system to reset target component on next loop
        self.mouse_x = -1
        self.mouse_y = -1

    # Handles right mouse button released
    def handle_right_mouse_released(self):
        if self.target_gizmo is not None:
            self.target_gizmo.handle_right_released()

        # Force system to reset target component on next loop
        self.mouse_x = -1
        self.mouse_y = -1

    # Generates an object ID
    @staticmethod
    def gen_obj_id():
        # Find lowest empty slot
        obj_index = -1
        for i in range(256):
            if GizmoSystem.gizmos[i] is None:
                obj_index = i
                break

        # Check if empty slot was found
        if obj_index == -1:
            raise Exception("Ran out of object slots")
        return obj_index

    # Frees an object ID for usage
    @staticmethod
    def free_obj_id(object_id):
        GizmoSystem.gizmos[object_id] = None

    # Adds a gizmo to the system
    @staticmethod
    def add_gizmo(gizmo):
        obj_id = GizmoSystem.gen_obj_id()
        gizmo.set_object_id(obj_id)
        GizmoSystem.gizmos[obj_id] = gizmo

    # Removes a gizmo from the system
    @staticmethod
    def remove_gizmo(gizmo):
        GizmoSystem.gizmos[gizmo.object_id] = None

    # Sets the current focused gizmo
    @staticmethod
    def set_focus(gizmo):
        if GizmoSystem.gizmo_system.focus_gizmo not in [gizmo, None]:
            GizmoSystem.gizmo_system.focus_gizmo.handle_lost_focus()
        GizmoSystem.gizmo_system.focus_gizmo = gizmo

    # Sets the current focused gizmo to none
    @staticmethod
    def release_focus():
        GizmoSystem.set_focus(None)

    # Sets the drag gizmo
    @staticmethod
    def set_drag(gizmo):
        GizmoSystem.gizmo_system.start_drag_x = GizmoSystem.gizmo_system.mouse_x
        GizmoSystem.gizmo_system.start_drag_y = GizmoSystem.gizmo_system.mouse_y
        GizmoSystem.gizmo_system.drag_gizmo = gizmo

    # Sets the current focused gizmo to none
    @staticmethod
    def release_drag():
        if GizmoSystem.gizmo_system.drag_gizmo is not None:
            GizmoSystem.gizmo_system.drag_gizmo.handle_drag_stop()
        GizmoSystem.set_drag(None)
