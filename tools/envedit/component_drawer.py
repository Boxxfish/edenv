"""
A GUI component that displays properties of the EDEnv component.

@author Ben Giacalone
"""
from tools.envedit.gui.gui_frame import GUIFrame
from tools.envedit.gui.gui_label import GUILabel
from tools.envedit.gui.gui_stack_layout import GUIStackLayout


class ComponentDrawer(GUIFrame):

    def __init__(self, component=None):
        GUIFrame.__init__(self)
        self.component = component

        # GUI settings
        self.fit_height_to_content = True
        self.padding = 10
        self.set_bg_color((1, 1, 1, 0.2))

        layout = GUIStackLayout()
        self.set_child(layout)

        self.title = GUILabel()
        self.title.text_size = 15
        self.title.set_text(self.component.name)
        layout.add_child(self.title)

        self.setup_drawer()

    # Sets up the component drawer
    def setup_drawer(self):
        pass



