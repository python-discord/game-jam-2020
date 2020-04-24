from pathlib import Path

import arcade
from screeninfo import get_monitors
from .Display import Button
from .Display import ColourBlend as cb


class SongSelection(arcade.View):

    width = 1920  # get_monitors()[0].width
    height = 1080  # get_monitors()[0].width

    def __init__(self, main):
        super().__init__()
        self.main = main
