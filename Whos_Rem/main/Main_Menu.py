from pathlib import Path

import arcade
from Display import Button
from Display import ColourBlend as cb


class MainMenu(arcade.View):
    width = 1920  # get_monitors()[0].width
    height = 1080  # get_monitors()[0].height

    mouse_x = 0
    mouse_y = 0
    mouse_pressing = False

    settings_button = Button(int(width*0.9), int(height*0.85),
                             int(width*0.1), int(height*0.1),
                             draw_func=lambda: None,
                             activation=lambda: print("uwu"))

    setting_button_image = arcade.Sprite(
        filename=Path().cwd() / Path("Resources/menu/settings_button.png"),
        scale=int(min(width, height)*0.15) / 256,
        center_x=int(width*0.925),
        center_y=int(height * 0.9),)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])
        arcade.draw_text("MENU", self.width*0.36, self.height*0.64,
                         color=cb.brightness([255, 255, 255], self.settings.brightness),
                         font_size=min(self.width, self.height)*0.15,
                         )
        self.setting_button_image.alpha = int(255*self.settings.brightness)
        self.setting_button_image.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.settings_button.pressed(x, y):
            window.show_view(self.settings)


if __name__ == "__main__":
    from Settings import Settings
    window = arcade.Window(MainMenu.width, MainMenu.height, "MENU")
    menu_view = MainMenu(Settings())
    window.show_view(menu_view)
    arcade.run()
