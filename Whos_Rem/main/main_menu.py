from pathlib import Path
import time
import math

import arcade
import pyautogui
from .display import Button
from .display import ColourBlend as cb


class SwayingNote:
    width, height = pyautogui.size()

    def __init__(self, x_pos, y_pos, path, rocking_rate=0.05):
        self.image = arcade.Sprite(
            filename=path,
            scale=int(min(self.width, self.height) * 0.2) / 512,
            center_x=x_pos,
            center_y=y_pos,
        )
        self.rocker = self.rocking(rocking_rate, max_angle=12)

    def draw(self, brightness):
        self.image.alpha = int(255*brightness)
        self.image.angle = next(self.rocker)
        self.image.draw()

    @staticmethod
    def rocking(inc=0.1, max_angle=1):
        val = 0
        while True:
            yield math.sin(val)*max_angle
            val += inc
            val %= math.pi * 2


class MainMenu(arcade.View):
    width, height = pyautogui.size()

    mouse_x = 0
    mouse_y = 0
    mouse_pressing = False

    background_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/background.png"),
        scale=max(width/6400, height/3600),
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

    note_1 = SwayingNote(width*0.1, height*0.75,
                         path=Path().cwd() / Path("main/Resources/main_menu/music_note_1.png"))
    note_2 = SwayingNote(width * 0.19, height * 0.25,
                         path=Path().cwd() / Path("main/Resources/main_menu/music_note_2.png"))
    note_3 = SwayingNote(width * 0.9, height * 0.55,
                         path=Path().cwd() / Path("main/Resources/main_menu/music_note_3.png"))

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
        self.note_1.draw(self.main.brightness)
        self.note_2.draw(self.main.brightness)
        self.note_3.draw(self.main.brightness)

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
