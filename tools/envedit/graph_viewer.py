"""
Controls the scene graph viewer.

@author Ben Giacalone
"""
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton
from direct.showbase.Loader import Loader, TextNode
from pathlib import Path
from panda3d.core import Filename
from os import path
from tools.envedit.graph_node import GraphNode


class GraphViewer:

    def __init__(self, base, render):
        # State vars
        self.render = render
        self.base = base
        self.scene_root = GraphNode(name="root")
        graph_a = GraphNode(name="Object A")
        graph_a.add_child(GraphNode(name="Object 1"))
        graph_a.add_child(GraphNode(name="Object 2"))
        self.scene_root.add_child(graph_a)
        self.scene_root.add_child(GraphNode(name="Object B"))

        # Load fonts
        font_path = Path(path.realpath(__file__)).parent.parent.parent / "res/fonts"
        font_loader = Loader(self.base)
        self.font_reg = font_loader.loadFont(Filename(font_path / "Jura/static/Jura-Regular.ttf").cStr())
        self.font_bold = font_loader.loadFont(Filename(font_path / "Jura/static/Jura-Bold.ttf").cStr())

        # Create frame to store object labels
        frame_size = 0.8 / 2
        self.frame = DirectFrame(frameColor=(0, 0, 0, 0.6),
                                 frameSize=(-frame_size, frame_size, -frame_size * 2.5, frame_size * 2.5),
                                 pos=(-.95, 0, 0))

        # Create graph viewer title
        self.title = DirectLabel(text="Scene Graph",
                                 parent=self.frame,
                                 scale=0.1,
                                 pos=(0, 0, 0.6),
                                 text_font=self.font_bold,
                                 text_fg=(1, 1, 1, 1),
                                 frameColor=(0, 0, 0, 0))

        # Set up scene tree
        self.root_label, _ = self.setup_scene_tree(self.scene_root, self.frame, 0)
        self.root_label.setScale(0.1)
        self.root_label.setPos(-0.3, 0, 0.4)

        self.frame.resetFrameSize()

    # Adds a node from the scene tree to the graph viewer.
    def setup_scene_tree(self, node, parent, index):
        # Create text label
        label = DirectButton(text=node.name,
                             parent=parent,
                             pos=(1, 0, (index + 1) * -1.2),
                             text_align=TextNode.ALeft,
                             text_font=self.font_reg,
                             text_fg=(1, 1, 1, 1),
                             frameColor=(0, 0, 0, 0))

        # Propagate to children
        c_index = 0
        for child in node.children:
            _, c_index = self.setup_scene_tree(child, label, c_index)

        return label, c_index + index + 1
