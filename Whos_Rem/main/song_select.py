from pathlib import Path

import arcade
from screeninfo import get_monitors
from .Display import Button
from .Display import ColourBlend as cb


class SongSelection(arcade.View):

    width = 1920  # get_monitors()[0].width
    height = 1080  # get_monitors()[0].width

    return_button_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/settings/return_button.png"),
        scale=int(min(width, height) * 0.15) / 512,
        center_x=int(width * 0.075),
        center_y=int(height * 0.9), )

    return_button = Button(width * 0.03, height * 0.86, width * 0.09, height * 0.08,
                           activation=lambda: None, draw_func=lambda: None, name="menu button")

    def __init__(self, main):
        super().__init__()
        self.main = main

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])

        self.return_button_image.alpha = int(255*self.main.brightness)
        self.return_button_image.draw()

    def on_mouse_press(self, x, y, button, modifiers):

        if self.return_button.pressed(x, y):
            self.main.window.show_view(self.main.menu)
