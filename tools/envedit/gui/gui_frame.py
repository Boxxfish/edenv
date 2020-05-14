"""
Base class for rendered components.

@author Ben Giacalone
"""
from os import path
from pathlib import Path

from direct.gui.DirectFrame import DirectFrame, Filename
from tools.envedit.gui.gui_component import GUIComponent
from tools.envedit.gui.panda_gui_utils import GUIUtils


class GUIFrame(GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)
        self.bg_color = (0, 0, 0, 0)
        self.bg_image = None
        self.padding = 0
        self.fit_width_to_content = False       # if the width should conform to the child
        self.fit_height_to_content = False      # if the height should conform to the child
        self.frame = None

    # Sets background color
    def set_bg_color(self, bg_color):
        self.bg_color = bg_color
        self.update()

    # Sets the background image
    def set_bg_image(self, image_path):
        image_folder_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/images"
        self.bg_image = Filename(image_folder_path / image_path).cStr()
        self.update()

    # Default behavior is to fill in the bounding box with bg color
    def update(self):
        if self.frame is not None:
            self.frame["frameColor"] = self.bg_color
            if self.bg_image is not None:
                self.frame["frameTexture"] = self.bg_image
            x, y, width, height = GUIUtils.get_panda_coords(self.bbox.x, self.bbox.y, self.bbox.width, self.bbox.height)
            self.frame.setPos(x, 0, y)
            self.frame["frameSize"] = (-width / 2, width / 2, -height / 2, height / 2)
            self.frame.resetFrameSize()
            if self.child is not None:
                self.child.bbox.x = self.bbox.x + self.padding
                self.child.bbox.y = self.bbox.y + self.padding
                if self.fit_width_to_content:
                    self.bbox.width = self.child.bbox.width + 2 * self.padding
                else:
                    self.child.bbox.width = self.bbox.width - 2 * self.padding
                if self.fit_height_to_content:
                    self.bbox.height = self.child.bbox.height + 2 * self.padding
                else:
                    self.child.bbox.height = self.bbox.height - 2 * self.padding

                self.child.update()

    def add_render(self):
        self.rendering = True
        self.frame = DirectFrame(frameSize=(-1, 1, 1, -1))
        if self.child is not None:
            self.child.add_render()
        self.update()

    def stop_render(self):
        if self.rendering:
            self.frame.destroy()
            self.frame = None
        self.rendering = False
        if self.child is not None:
            self.child.stop_render()
        self.update()
