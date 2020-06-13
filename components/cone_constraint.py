"""
Cone constraint for the physics engine.

"""
import numpy as np
from panda3d.bullet import BulletRigidBodyNode, BulletConeTwistConstraint
from panda3d.core import LVector3f, TransformState

from components.rigidbody import Rigidbody
from tools.envedit import helper
from tools.envedit.edenv_component import EComponent
from tools.envedit.property_type import PropertyType
from tools.run.event import handler


class ConeConstraint(EComponent):

    def __init__(self):
        EComponent.__init__(self)

    @staticmethod
    def get_properties():
        return {"axis": PropertyType.VECTOR3,
                "swing_1": PropertyType.FLOAT,
                "swing_2": PropertyType.FLOAT,
                "max_twist": PropertyType.FLOAT}

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
                child_transform = TransformState.make_pos(LVector3f(0, 0, 0))
                node_pos = self.node.transform.get_translation() * self.node.transform.get_world_scale()
                parent_transform = TransformState.make_pos(helper.np_vec3_to_panda(node_pos))
                constraint = BulletConeTwistConstraint(component.body_path.node(),
                                                       self.parent_path.node(),
                                                       child_transform,
                                                       parent_transform)
                constraint.set_limit(float(self.property_vals["swing_1"]),
                                     float(self.property_vals["swing_2"]),
                                     float(self.property_vals["max_twist"]))
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