"""
Point constraint for the physics system.

"""
import numpy as np
from panda3d.bullet import BulletSphericalConstraint, BulletRigidBodyNode
from panda3d.core import PandaNode, LVector3f, LPoint3f

from components.rigidbody import Rigidbody
from tools.envedit import helper
from tools.envedit.edenv_component import EComponent
from tools.run.event import handler


class PointConstraint(EComponent):

    def __init__(self):
        EComponent.__init__(self)
        self.parent_path = None
        self.update_parent = True

    @staticmethod
    def get_properties():
        return {}

    def start(self):
        for component in self.node.data:
            if isinstance(component, Rigidbody):
                # Check if parent has rigidbody, and use that node if it does
                for p_component in self.node.parent.data:
                    if isinstance(p_component, Rigidbody):
                        self.parent_path = p_component.body_path
                        self.update_parent = False

                if self.parent_path is None:
                    parent_node = BulletRigidBodyNode(self.node.parent.name + "_node")
                    parent_node.set_mass(0)
                    self.parent_path = EComponent.panda_root_node.attach_new_node(parent_node)

                self.parent_path.setPos(helper.np_vec3_to_panda(self.node.parent.transform.get_world_translation()))
                rot = np.degrees(self.node.parent.transform.get_world_rotation())
                self.parent_path.setHpr(LVector3f(rot[1],
                                                  rot[0],
                                                  rot[2]))
                self.parent_path.setScale(helper.np_vec3_to_panda(self.node.parent.transform.get_world_scale()))

                # Create constraint
                node_pos = self.node.transform.get_translation() * self.node.transform.get_world_scale()
                constraint = BulletSphericalConstraint(component.body_path.node(),
                                                       self.parent_path.node(),
                                                       LVector3f(0, 0, 0),
                                                       LVector3f(node_pos[0], node_pos[1], node_pos[2]))
                EComponent.physics_world.attachConstraint(constraint)

    @handler()
    def handle_update(self):
        # Update parent node
        if self.update_parent:
            self.parent_path.setPos(helper.np_vec3_to_panda(self.node.parent.transform.get_world_translation()))
            rot = np.degrees(self.node.parent.transform.get_world_rotation())
            self.parent_path.setHpr(LVector3f(rot[1],
                                              rot[0],
                                              rot[2]))
            self.parent_path.setScale(helper.np_vec3_to_panda(self.node.parent.transform.get_world_scale()))
