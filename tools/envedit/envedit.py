"""
Environment editor for EDEnv.

@author Ben Giacalone
"""

from direct.showbase.ShowBase import ShowBase
from tools.envedit.camera_controller import CameraController
from tools.envedit.floor_node import FloorNode

class EnvEdit(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Initial scene setup
        # self.disableMouse()

        # Add floor
        self.floor_node = FloorNode(self)
        floor_path = self.render.attach_new_node(self.floor_node)
        floor_path.setTwoSided(True)

        # Add camera controller
        # self.cam_controller = CameraController(self, self.camera)

if __name__ == "__main__":
    app = EnvEdit()
    app.run()
