"""
Loads fonts from a file.
GUIFontLoader abstracts the font loading process, so if EDEnv no longer uses
Panda3d, only this class needs to be rewritten.

@author Ben Giacalone
"""
from os import path
from pathlib import Path

from direct.showbase.Loader import Loader, Filename


class GUIFontLoader:
    base = None

    # Loads font from EDEnv's resource folder
    @staticmethod
    def load_font(font_path):
        font_folder_path = Path(path.realpath(__file__)).parent.parent.parent.parent / "res/fonts"
        font_loader = Loader(GUIFontLoader.base)
        return font_loader.loadFont(Filename(font_folder_path / font_path).cStr())
