"""
A component that renders read-only text.

@author Ben Giacalone
"""
from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode, LVector3f, ScissorAttrib, LVector4f

from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_system import GUISystem
from tools.envedit.gui.panda_gui_utils import GUIUtils


class GUILabel(GUIFrame):

    def __init__(self):
        GUIFrame.__init__(self)
        self.text = ""
        self.font = GUISystem.get_font("default")
        self.text_color = (1, 1, 1, 1)
        self.bg_color = (1, 0, 1, 0)
        self.text_size = 12
        self.frame = None

    def update(self):
        if self.frame is not None:
            self.frame["text"] = self.text
            self.frame["text_fg"] = self.text_color
            self.frame["frameColor"] = self.bg_color
            self.frame["text_font"] = self.font

            bounds = self.frame.getBounds()
            scale = (self.text_size * 2.5) / (GUIUtils.square_size + 1)
            self.bbox.width, self.bbox.height = GUIUtils.get_screen_space_size((bounds[1] - bounds[0]) * scale,
                                                                               (bounds[3] - bounds[2]) * scale)
            x, y, width, height = GUIUtils.get_panda_text_coords(self.bbox.x,
                                                                 self.bbox.y,
                                                                 self.bbox.width,
                                                                 self.bbox.height)
            self.frame.setPos(x, 0, y)
            self.frame.setScale(scale)

            # Set up scissor test
            clip_x, clip_y, clip_w, clip_h = GUIUtils.get_panda_clip_coords(self.clip_region.x,
                                                                            self.clip_region.y,
                                                                            self.clip_region.width,
                                                                            self.clip_region.height)
            render_attrib = ScissorAttrib.make(LVector4f(clip_x, clip_x + clip_w, clip_y - clip_h, clip_y))
            self.frame.setAttrib(render_attrib)

    def set_text(self, text):
        self.text = text
        self.update()

    def set_text_color(self, color):
        self.text_color = color
        self.update()

    def set_font(self, font):
        self.font = font
        self.update()

    def add_render(self):
        self.rendering = True
        self.frame = DirectLabel(text_font=self.font,
                                 text_align=TextNode.ALeft,
                                 text_fg=self.text_color,
                                 frameColor=self.bg_color,
                                 text=self.text)
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
