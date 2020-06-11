"""
Rigidbody for the physics engine.

"""
import numpy as np
from panda3d.bullet import BulletRigidBodyNode
from panda3d.core import LVector3f

from tools.envedit import helper
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType
from tools.run.event import handler


class Rigidbody(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.body_path = None

    @staticmethod
    def get_properties():
        return {"mass": PropertyType.FLOAT}

    def start(self):
        body_node = BulletRigidBodyNode(self.node.name + "_rigid_body")
        body_node.set_mass(float(self.property_vals["mass"]))
        self.body_path = EComponent.panda_root_node.attach_new_node(body_node)
        self.body_path.setPos(helper.np_vec3_to_panda(self.node.transform.get_world_translation()))
        rot = np.degrees(self.node.transform.get_world_rotation())
        self.body_path.setHpr(LVector3f(rot[1],
                                        rot[0],
                                        rot[2]))
        self.body_path.setScale(helper.np_vec3_to_panda(self.node.transform.get_world_scale()))
        EComponent.physics_world.attachRigidBody(body_node)

    @handler()
    def handle_update(self):
        if self.body_path is not None:
            self.node.transform.set_matrix(helper.panda_mat4_to_np(self.body_path.getMat()))
