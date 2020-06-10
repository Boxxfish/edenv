"""
Actually plays out trials.

@author Ben Giacalone
"""
import json
from pathlib import Path
import sys
import yaml
from direct.showbase.ShowBase import ShowBase
from panda3d.core import PandaNode, DirectionalLight
from tools.envedit.camera_controller import CameraController
from tools.envedit.edenv_component import EComponent
from tools.envedit.floor_node import FloorNode
from tools.envedit.graph_node import GraphNode


class Player(ShowBase):

    def __init__(self, env_name):
        ShowBase.__init__(self)

        # Initial scene setup
        self.disableMouse()
        self.setBackgroundColor(0.15, 0.15, 0.15, 1)
        EComponent.panda_root_node = self.render.attach_new_node(PandaNode("Root"))
        EComponent.base = self

        # Attach a directional light to the camera
        self.dir_light = DirectionalLight("cam_dir_light")
        dir_light_path = self.camera.attach_new_node(self.dir_light)
        EComponent.panda_root_node.setLight(dir_light_path)

        # Read the project config file
        config_path = Path("project.yaml")
        config = None
        if not config_path.exists():
            sys.stderr.write("Error: Could not find project.yaml.")
            return
        with open("project.yaml", "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        # Add floor
        self.floor_node = FloorNode(self)
        floor_path = self.render.attach_new_node(self.floor_node)
        floor_path.setTwoSided(True)
        floor_path.set_shader_input("object_id", 0)

        # Add camera controller
        self.cam_controller = CameraController(self, self.render, self.camera)

        # Load environment
        with open(env_name + ".json", "r") as file:
            scene_dict = json.load(file)
            self.root_node = GraphNode.dict_to_scene_graph(scene_dict, use_gui=False)

            self.start_node(self.root_node)

    # Starts all nodes
    def start_node(self, node):
        node.start_components()
        for child in node.children:
            self.start_node(child)


def run(env_name):
    app = Player(env_name)
    app.run()
