"""
Provides methods for interacting with the physics engine.

@author Ben Giacalone
"""
from tools.envedit import helper


class Physics:

    def __init__(self, physics_world):
        self.physics_world = physics_world

    # Performs a raycast against objects in the scene
    def raycast(self, ray_origin, ray_dir):
        # Perform raycast
        result = self.physics_world.rayTestClosest(helper.np_vec3_to_panda(ray_origin),
                                                   helper.np_vec3_to_panda(ray_origin + ray_dir * 9999))
        if not result.hasHit():
            return None

        # Return a RaycastResult object
        raycast_obj = RaycastResult()
        raycast_obj.hit_node_id = result.getNode().name[:-11]
        raycast_obj.hit_point = helper.panda_vec3_to_np(result.getHitPos())
        return raycast_obj

class RaycastResult:

    def __init__(self):
        self.hit_node_id = None
        self.hit_point = None
