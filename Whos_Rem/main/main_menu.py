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

    settings_button = Button(int(width*0.9), int(height*0.85),
                             int(width*0.1), int(height*0.1),
                             draw_func=lambda: None,
                             activation=lambda: None)

    setting_button_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/menu/settings_button.png"),
        scale=int(min(width, height)*0.15) / 256,
        center_x=int(width*0.925),
        center_y=int(height * 0.9),)

    select_song_button = Button(int(width*0.3), int(height*0.2), int(width*0.4), int(height*0.35),
                                draw_func=lambda: None,
                                activation=lambda: None)

    menu_text_colour = cb.rainbow_cycle(step=8)

    def __init__(self, main):
        super().__init__()
        self.main = main

    def on_update(self, delta_time):
        time.sleep(max(0, 0.1 - delta_time))
        self.on_draw()

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])
        arcade.draw_text("3 STRINGS", self.width*0.23, self.height*0.64,
                         color=cb.brightness(next(self.menu_text_colour), self.main.brightness),
                         font_size=min(self.width, self.height)*0.18,
                         )
        self.setting_button_image.alpha = int(255*self.main.brightness)
        self.setting_button_image.draw()

        arcade.draw_rectangle_outline(int(self.width*0.5), int(self.height*0.4),
                                      int(self.width*0.4), int(self.height*0.35),
                                      color=cb.brightness([255, 255, 255], self.main.brightness),
                                      border_width=min(self.width, self.height)*0.02)

        arcade.draw_text("SELECT A\n   SONG", int(self.width * 0.33), int(self.height * 0.25),
                         color=cb.brightness([255, 255, 255], self.main.brightness),
                         font_size=min(self.width, self.height)*0.13)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.settings_button.pressed(x, y):
            self.main.window.show_view(self.main.settings)
        elif self.select_song_button.pressed(x, y):
            self.main.window.show_view(self.main.song_selection)
