"""
Handles 3D object selection.

@author Ben Giacalone
"""
from os import path
from pathlib import Path

from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import Shader, PNMImage, Filename, NodePath

from tools.envedit.selectable_object import SelectableObject


class ObjectSelector(DirectObject):
    selectable_objects = [None for _ in range(256)]

    def __init__(self, base, envedit_data):
        self.base = base
        self.envedit_data = envedit_data
        self.target_object_id = 0
        self.selected_object_id = 0

        # Create frame buffer
        self.frame_buffer = self.base.win.makeTextureBuffer("Color Picker Buffer", 512, 512, to_ram=True)
        self.frame_buffer.setSort(-100)
        self.frame_buffer.setClearColor((0, 0, 0, 1))

        # Load object selection shader
        shader_folder_path = Path(path.realpath(__file__)).parent.parent.parent / "res/shaders"
        self.color_picker_shader = Shader.load(Shader.SL_GLSL,
                                               vertex=Filename(shader_folder_path / "picker.vert").cStr(),
                                               fragment=Filename(shader_folder_path / "picker.frag").cStr())

        # Set up color picking camera
        self.color_cam = self.base.makeCamera(self.frame_buffer)
        color_cam_options = NodePath("color_cam_options")
        color_cam_options.setShader(self.color_picker_shader)
        self.color_cam.node().setInitialState(color_cam_options.getState())

        # Register events
        self.accept("mouse1", self.handle_left_mouse_pressed)
        self.accept("mouse1-up", self.handle_left_mouse_released)

        # Remove the background from selecting
        ObjectSelector.selectable_objects[0] = SelectableObject()

        # Add object selection task
        self.add_task(self.handle_object_selection)

    # Task to handle object selection
    def handle_object_selection(self, task):
        # Get mouse screen space coords
        mouse_x = 0
        mouse_y = 0
        if self.base.mouseWatcherNode.hasMouse():
            mouse_x = int(512 * ((self.base.mouseWatcherNode.getMouseX() + 1) / 2))
            mouse_y = int(512 * (1 - (self.base.mouseWatcherNode.getMouseY() + 1) / 2))

        # Extract texture
        frame_texture = self.frame_buffer.getTexture()
        frame_pnm = PNMImage()
        frame_texture.store(frame_pnm)

        # Get object ID
        if 0 < mouse_x < 512 and 0 < mouse_y < 512:
            object_id = frame_pnm.getPixel(mouse_x, mouse_y)[0]
            self.target_object_id = object_id

        return Task.cont

    # "Destructor" for object selector
    def destroy(self):
        self.ignore_all()

    # Handles left mouse button pressed
    def handle_left_mouse_pressed(self):
        if self.target_object_id == 0:
            return

        self.set_selected_obj(ObjectSelector.selectable_objects[self.target_object_id])

    # Handles left mouse button released
    def handle_left_mouse_released(self):
        if self.target_object_id == 0:
            return

        obj = ObjectSelector.selectable_objects[self.target_object_id]
        obj.on_released()

    # Sets the currently selected object
    def set_selected_obj(self, selectable_object):
        former_obj = ObjectSelector.selectable_objects[self.selected_object_id]
        curr_obj = ObjectSelector.selectable_objects[selectable_object.get_object_id()]

        self.selected_object_id = curr_obj.get_object_id()
        former_obj.on_deselected()
        curr_obj.on_pressed()

    # Updates the object selector
    def update_selector(self):
        if self.envedit_data.target_node is not None and self.envedit_data.target_node.object_id is not self.selected_object_id:
            target_node_id = self.envedit_data.target_node.object_id
            self.set_selected_obj(ObjectSelector.selectable_objects[target_node_id])

    # Generates an object ID
    @staticmethod
    def gen_obj_id():
        # Find lowest empty slot
        obj_index = -1
        for i in range(256):
            if ObjectSelector.selectable_objects[i] is None:
                obj_index = i
                break

        # Check if empty slot was found
        if obj_index == -1:
            raise Exception("Ran out of object slots")
        return obj_index

    # Frees an object ID for usage
    @staticmethod
    def free_obj_id(object_id):
        ObjectSelector.selectable_objects[object_id] = None

    # Generates a new selectable object
    @staticmethod
    def gen_selectable_obj(mesh_json=None):
        obj = SelectableObject(mesh_json)
        obj_id = ObjectSelector.gen_obj_id()
        obj.set_object_id(obj_id)
        ObjectSelector.selectable_objects[obj_id] = obj
        return obj

    # Destroys a selectable object
    @staticmethod
    def destroy_selectable_obj(selectable_object):
        ObjectSelector.free_obj_id(selectable_object.get_object_id())
        selectable_object.destroy()
