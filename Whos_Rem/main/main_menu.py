from pathlib import Path
import time

import arcade
import pyautogui
from .display import Button
from .display import ColourBlend as cb


class MainMenu(arcade.View):
    width, height = pyautogui.size()

    mouse_x = 0
    mouse_y = 0
    mouse_pressing = False

    background_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/background.png"),
        scale=min(width / 6400, height / 3600),
        center_x=int(width * 0.5),
        center_y=int(height * 0.5),
    )

    settings_button = Button(int(width*0.9), int(height*0.85),
                             int(width*0.1), int(height*0.1),
                             draw_func=lambda: None,
                             activation=lambda: None)

    settings_button_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/main_menu/settings_button.png"),
        scale=int(min(width, height)*0.15) / 256,
        center_x=int(width*0.925),
        center_y=int(height * 0.9),)

    select_song_button = Button(int(width*0.3), int(height*0.2), int(width*0.4), int(height*0.35),
                                draw_func=lambda: None,
                                activation=lambda: None)

    menu_title = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/main_menu/3-Strings.png"),
        scale=int(min(width, height)*0.5) / 256,
        center_x=int(width*0.5),
        center_y=int(height * 0.75),
    )
    select_song_text = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/main_menu/Select-Song.png"),
        scale=int(min(width, height) * 0.4) / 256,
        center_x=int(width * 0.5),
        center_y=int(height * 0.4),
    )

    def __init__(self, main):
        super().__init__()
        self.main = main

    def on_update(self, delta_time):
        time.sleep(max(0, 0.1 - delta_time))
        self.on_draw()

    def on_draw(self):
        arcade.start_render()
        self.background_image.alpha = int(255 * self.main.brightness)
        self.background_image.draw()

        self.settings_button_image.alpha = int(255 * self.main.brightness)
        self.settings_button_image.draw()

        arcade.draw_rectangle_outline(int(self.width*0.5), int(self.height*0.4),
                                      int(self.width*0.4), int(self.height*0.35),
                                      color=cb.brightness([255, 255, 255], self.main.brightness),
                                      border_width=min(self.width, self.height)*0.02)

        self.draw_text()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.settings_button.pressed(x, y):
            self.main.window.show_view(self.main.settings)
        elif self.select_song_button.pressed(x, y):
            self.main.window.show_view(self.main.song_selection)

    def draw_text(self):
        alpha = int(255 * self.main.brightness)
        self.settings_button_image.alpha = alpha
        self.settings_button_image.draw()

        self.menu_title.alpha = alpha
        self.menu_title.draw()

        self.select_song_text.alpha = alpha
        self.select_song_text.draw()
