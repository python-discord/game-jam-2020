from pathlib import Path

import arcade
import pyautogui
from .display import Button
from .display import ColourBlend as cb


class SongChoices:

    names_dict = {
        1: "MEGALOVANIA (Camellia Remix)",
        2: "Camellia - Light it up",
        3: "Getsix - Sky Fracture VIP (feat. Miss Lina)",
        4: "The Fat Rat - Stronger",
    }
    screen_size = pyautogui.size()

    def __init__(self, song_id: int, colour: list):
        self.song_id = song_id
        self.name = f"{self.song_id}: {self.names_dict.get(song_id, '')}"
        self.width = self.screen_size[0]*0.7
        self.height = self.screen_size[1]*0.08
        self.font_size = self.height * 0.45
        self.x_pos = self.screen_size[0]*0.05
        self.y_pos = self.screen_size[1]*(0.7 - 0.12*song_id)
        self.colour = colour

    def draw(self, brightness):
        arcade.draw_lrtb_rectangle_filled(self.x_pos, self.x_pos + self.width,
                                          self.y_pos + self.height, self.y_pos,
                                          cb.brightness(self.colour, brightness))
        arcade.draw_text(self.name, self.x_pos + self.width*0.03, self.y_pos + self.height*0.17,
                         cb.brightness(cb.invert(self.colour), brightness), self.font_size)

    def clicked(self, mouse_x, mouse_y):
        if 0 <= mouse_x - self.x_pos <= self.width:
            if 0 <= mouse_y - self.y_pos <= self.height:
                return True

        return False

    def generate_song_data(self):
        return SongSelection.load_song_data(self.song_id)

    @classmethod
    def manage_song_selections(cls, song_list: "list of SongChoices instances", mouse_x, mouse_y):
        song_dict = None
        for item in song_list:
            if item.clicked(mouse_x, mouse_y):
                song_dict = item.generate_song_data()
                print(song_dict)

        return song_dict

    @classmethod
    def draw_song_choices(cls, song_list: "list of SongChoices instances", brightness):
        for song in song_list:
            song.draw(brightness)


class SongSelection(arcade.View):

    width, height = pyautogui.size()

    return_button_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/settings_menu/return_button.png"),
        scale=int(min(width, height) * 0.15) / 512,
        center_x=int(width * 0.075),
        center_y=int(height * 0.9),
    )
    background_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/background.png"),
        scale=max(width/6400, height/3600),
        center_x=int(width * 0.5),
        center_y=int(height * 0.5),
    )

    return_button = Button(width * 0.03, height * 0.86, width * 0.09, height * 0.08,
                           activation=lambda: None, draw_func=lambda: None, name="menu button")

    songs = [SongChoices(num, [0, 0, 0]) for num in range(1, 6)]

    def __init__(self, main):
        super().__init__()
        self.main = main

    def on_draw(self):
        arcade.start_render()
        self.background_image.alpha = int(255 * self.main.brightness)
        self.background_image.draw()

        arcade.draw_text("Choose a song:", self.width*0.05, self.height*0.67,
                         cb.brightness([255, 255, 255], self.main.brightness),
                         font_size=min(self.width, self.height)*0.1,)
        self.return_button_image.alpha = int(255*self.main.brightness)
        self.return_button_image.draw()

        SongChoices.draw_song_choices(self.songs, self.main.brightness)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.return_button.pressed(x, y):
            self.main.window.show_view(self.main.menu)

        choice = SongChoices.manage_song_selections(self.songs, x, y)
        if choice is not None:
            self.main.play_screen.setup(choice)
            self.main.window.show_view(self.main.play_screen)

    @staticmethod
    def load_song_data(song_choice, base_path=Path.cwd() / Path("main/tracks")):
        name = SongChoices.names_dict.get(song_choice, f"track_{song_choice}")
        file_type = list(base_path.glob(f"*track_{song_choice}*"))
        file_type = [path.suffix[1:] for path in file_type if "json" not in path.suffix]
        track_dict = {
            "name": name,
            "path": f"track_{song_choice}",
            "type": file_type[0]
        }

        return track_dict
