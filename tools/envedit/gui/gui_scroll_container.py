"""
A container for scrolled content.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_dock_layout import GUIDockLayout
from tools.envedit.gui.gui_scrollbar import GUIScrollbar


class GUIScrollContainer(GUIDockLayout):

    def __init__(self, scroll_v=True, scroll_h=False):
        GUIDockLayout.__init__(self)
        self.scroll_v = scroll_v
        self.scroll_h = scroll_h
        self.v_offset = 0
        self.h_offset = 0
        self.v_offset_per_scroll = 0
        self.h_offset_per_scroll = 0
        self.vertical_scrollbar = None
        self.horizontal_scrollbar = None

        if self.scroll_v:
            self.vertical_scrollbar = GUIScrollbar()
            self.vertical_scrollbar.on_scroll = self.v_scroll_handler
            self.set_child_dock(self.vertical_scrollbar, GUIDockLayout.RIGHT)

        if self.scroll_h:
            self.horizontal_scrollbar = GUIScrollbar(False)
            self.horizontal_scrollbar.on_scroll = self.h_scroll_handler
            self.set_child_dock(self.horizontal_scrollbar, GUIDockLayout.BOTTOM)

    def update(self):
        GUIDockLayout.update(self)

        self.center_child.bbox.y = self.bbox.y - self.v_offset
        self.center_child.bbox.x = self.bbox.x - self.h_offset

        if self.scroll_v and self.center_child is not None and self.vertical_scrollbar is not None:
            self.v_offset_per_scroll = self.center_child.bbox.height / (self.vertical_scrollbar.bbox.height + 0.001)
            if self.v_offset_per_scroll < 1:
                self.vertical_scrollbar.scroll_size = 0
            else:
                self.vertical_scrollbar.scroll_size = self.vertical_scrollbar.bbox.height - (self.center_child.bbox.height - self.vertical_scrollbar.bbox.height) / self.v_offset_per_scroll

        if self.scroll_h and self.center_child is not None and self.horizontal_scrollbar is not None:
            self.h_offset_per_scroll = self.center_child.bbox.width / (self.horizontal_scrollbar.bbox.width + 0.001)
            if self.h_offset_per_scroll < 1:
                self.horizontal_scrollbar.scroll_size = 0
            else:
                self.horizontal_scrollbar.scroll_size = self.horizontal_scrollbar.bbox.width - (self.center_child.bbox.width - self.horizontal_scrollbar.bbox.width) / self.h_offset_per_scroll

        self.center_child.set_clip_region(self.clip_region.get_intersection(self.bbox))
        self.center_child.update()

    def set_child(self, child):
        self.set_child_dock(child, GUIDockLayout.CENTER)

    def v_scroll_handler(self, offset):
        self.v_offset = offset * self.v_offset_per_scroll
        self.update()

    def h_scroll_handler(self, offset):
        self.h_offset = offset * self.h_offset_per_scroll
        self.update()
