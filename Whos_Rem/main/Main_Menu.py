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

    setting_button = arcade.Sprite(
        filename=f"{cwd}/Resources/menu/settings_button.png",
        scale=int(min(width, height)*0.15) / 256,
        center_x=int(width*0.925),
        center_y=int(height * 0.9),)

    @classmethod
    def on_draw(cls):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])
        arcade.draw_text("MENU", cls.width*0.36, cls.height*0.64,
                         color=[255, 255, 255],
                         font_size=min(cls.width, cls.height)*0.15,
                         )
        cls.setting_button.alpha = int(255*Settings().brightness)
        cls.setting_button.draw()


if __name__ == "__main__":
    window = arcade.Window(MainMenu.width, MainMenu.height, "MENU")
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()
