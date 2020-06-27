"""
Actually plays out trials.

@author Ben Giacalone
"""
import json
from pathlib import Path
import sys
import yaml
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.Task import Task
from panda3d.bullet import BulletWorld
from panda3d.core import PandaNode, DirectionalLight, LVector3f
from tools.envedit.camera_controller import CameraController
from tools.envedit.edenv_component import EComponent
from tools.envedit.floor_node import FloorNode
from tools.envedit.gizmos.gizmo_system import GizmoSystem
from tools.envedit.graph_node import GraphNode
from tools.run import event
from tools.run.event import register_component
from tools.run.trial import Trial


class Player(ShowBase):

    def __init__(self, env_name, trial_data, headless=False):
        self.manually_quit = True
        try:
            ShowBase.__init__(self, windowType="none" if headless else "onscreen")
        except:
            self.trial_finished_callback()

        # Allows importing components from project folder
        sys.path.append(".")

        # Initial scene setup
        self.disableMouse()
        self.setBackgroundColor(0.15, 0.15, 0.15, 1)
        EComponent.panda_root_node = self.render.attach_new_node(PandaNode("Root"))
        EComponent.base = self

        # Attach a directional light to the camera
        if not headless:
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
        if not headless:
            self.floor_node = FloorNode(self)
            floor_path = self.render.attach_new_node(self.floor_node)
            floor_path.setTwoSided(True)
            floor_path.set_shader_input("object_id", 0)

        # Add camera controller
        if not headless:
            self.cam_controller = CameraController(self, self.render, self.camera)

        # Set up physics system
        self.physics_world = BulletWorld()
        self.physics_world.setGravity(LVector3f(0, 0, -9.81))
        EComponent.physics_world = self.physics_world
        self.taskMgr.add(self.physics_task, "physics_task")

        # Load environment
        with open(env_name + ".json", "r") as file:
            scene_dict = json.load(file)
            self.root_node = GraphNode.dict_to_scene_graph(scene_dict, use_gui=False)

            trial = Trial()
            trial.data = trial_data
            trial.trial_finished_callback = self.trial_finished_callback
            self.setup_node(self.root_node, trial)

        # Set up update task
        self.taskMgr.add(self.update_task, "update_task")

    # Sets up all nodes
    def setup_node(self, node, trial):
        for component in node.data:
            # Register components to event system
            register_component(component)

            # Set trial property of components
            component.trial = trial

        # Start all the components
        node.start_components()

        # Propagate to children
        for child in node.children:
            self.setup_node(child, trial)

    # Updates components every frame
    def update_task(self, task):
        event.send_event("main", "update")
        return Task.cont

    # Updates the physics engine
    def physics_task(self, task):
        dt = globalClock.getDt()
        self.physics_world.doPhysics(dt)
        return Task.cont

    # Called when trial is finished
    def trial_finished_callback(self):
        self.manually_quit = False
        self.taskMgr.remove("update_task")
        self.taskMgr.remove("physics_task")
        event.COMPONENTS.clear()
        GizmoSystem.gizmos = [None for _ in range(256)]
        sys.exit()


def run(env_name, trial_data):
    app = Player(env_name, trial_data, headless=False)
    try:
        app.run()
    except SystemExit as e:
        if app.manually_quit:
            sys.exit()
        else:
            app.destroy()


def run_headless(env_name, trial_data):
    app = Player(env_name, trial_data, headless=True)
    try:
        app.run()
    except SystemExit as e:
        if app.manually_quit:
            sys.exit()
        else:
            app.destroy()
