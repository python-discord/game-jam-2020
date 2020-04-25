from pathlib import Path

import arcade
import pyautogui
from .display import Button
from .display import ColourBlend as cb


class SongSelection(arcade.View):

    width, height = pyautogui.size()

    return_button_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/settings_menu/return_button.png"),
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

        arcade.draw_text("Choose a song:", self.width*0.05, self.height*0.67,
                         cb.brightness([255, 255, 255], self.main.brightness),
                         font_size=min(self.width, self.height)*0.1,)
        self.return_button_image.alpha = int(255*self.main.brightness)
        self.return_button_image.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.return_button.pressed(x, y):
            self.main.window.show_view(self.main.menu)

    @staticmethod
    def load_song_data(song_choice, base_path=Path.cwd() / Path("main/tracks")):
        name = f"track_{song_choice}"
        file_type = list(base_path.glob(f"*{name}*"))
        file_type = [path.suffix[1:] for path in file_type if "json" not in path.suffix]
        track_dict = {
            "name": name,
            "path": base_path / Path(name),
            "type": file_type[0]
        }

        return track_dict
