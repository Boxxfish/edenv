"""
Environment editor for EDEnv.

@author Ben Giacalone
"""

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import pi, cos, sin
from tools.envedit.camera_controller import CameraController


class EnvEdit(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Initial scene setup
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        self.disableMouse()

        # Camera controller
        self.cam_controller = CameraController(self, self.camera)

if __name__ == "__main__":
    app = EnvEdit()
    app.run()
