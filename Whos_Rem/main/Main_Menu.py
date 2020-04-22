import os

import arcade
from Display import Button
from Display import ColourBlend as cb
from Settings import Settings


class MainMenu(arcade.View):
    width = 1920  # get_monitors()[0].width
    height = 1080  # get_monitors()[0].height

    mouse_x = 0
    mouse_y = 0
    mouse_pressing = False

    cwd = os.getcwd()

    background_sprite = arcade.Sprite(
        filename=f"{cwd}/Resources/menu/settings_button.png",
        scale=1,
        image_height=height,
        image_width=width)

    @classmethod
    def on_draw(cls):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])
        cls.background_sprite.draw()


if __name__ == "__main__":
    window = arcade.Window(Settings.width, Settings.height, "SETTINGS TEST")
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()
