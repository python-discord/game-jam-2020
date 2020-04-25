import arcade
from perspective_objects import ShapeManager
import itertools
import json
import time
import os

BASE_DIR = os.getcwd()
print(BASE_DIR)
song_filepath = r"TRACK_1.wav"
notes_filepath = r"track_1.json"

SPRITE_SCALING = 0.5
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

key_binds = {"left": arcade.key.A, "center": arcade.key.S, "right": arcade.key.D}


class GameScreen(arcade.View):
    """
    This should render at 32 fps or 16 fps (32fps is best), this is so
    the audio bars sync up in the right time frame, Musically speaking
    on a 4/4 beat.
    """
    width = 1000  # get_monitors()[0].width
    height = 600  # get_monitors()[0].height

    left_button_active = False
    middle_button_active = False
    right_button_active = False

    paused = started = False

    left = center = right = False
    with open(f"{BASE_DIR}/tracks/{notes_filepath}", 'r') as file:
        notes = json.load(file)
    frame_count = itertools.count(0, 1)
    all_sprites_list = arcade.SpriteList()
    background_sprite = arcade.Sprite(
        filename=f"{BASE_DIR}/Resources/game_play/undertale.png",
        scale=1,
        image_height=height,
        image_width=width)

    song = arcade.Sound(f"{BASE_DIR}/tracks/{song_filepath}",
                        streaming=True)

    # settings
    no_fail = True  # no matter how many times u miss you're not gonna loose
    fps = 16  # used for calculations
    active = False

    def setup(self):
        arcade.schedule(self.on_draw, 1 / self.fps)
        self.song.play(0.05)
        self.active = True
        time.sleep(0.03)

    @staticmethod
    def draw_note_key(x, y, height, width):
        arcade.draw_rectangle_filled(x, y, width=width, height=height, color=arcade.color.CRIMSON)

    def get_notes(self, frame):
        section, frame = divmod(frame, self.fps)
        return self.notes[section][frame]

    def on_update(self, delta_time: float):
        """ In charge of registering if a user had hit or missed a note. """

        total_secs = self.song.get_stream_position()
        if total_secs <= 0:
            self.active = False

        if (total_secs < self.song.get_length()) and self.active:
            self.left, self.center, self.right = self.get_notes(next(self.frame_count))

            # for testing only:
            self.left_button_active = self.left
            self.middle_button_active = self.center
            self.right_button_active = self.right

    def on_draw(self, time_delta=None):
        """ In charge of rendering the notes at current time. """
        arcade.start_render()

        if not self.paused:
            arcade.draw_rectangle_filled(
                self.width / 2,
                self.height / 2,
                width=self.width / 2,
                height=self.height,
                color=arcade.color.WHITE)
            self.background_sprite.center_x = self.width / 2
            self.background_sprite.center_y = self.height / 2
            self.background_sprite.scale = 1
            self.background_sprite.width = self.width / 2
            self.background_sprite.alpha = 160
            self.background_sprite.draw()

            arcade.draw_rectangle_filled(
                self.width / 2,
                self.height / 10,
                width=self.width / 2,
                height=self.height / 4,
                color=arcade.color.WHITE)
            self.started = True

        if self.left_button_active:
            self.draw_note_key(self.width / 2 - 105, self.height / 10, self.height / 4, self.width / 10)

        if self.middle_button_active:
            self.draw_note_key(self.width / 2, self.height / 10, self.height / 4, self.width / 10)

        if self.right_button_active:
            self.draw_note_key(self.width / 2 + 105, self.height / 10, self.height / 4, self.width / 10)

    def on_key_press(self, symbol: int, modifiers: int):
        """ This is only for registering if keys are pressed and to change the relevant buttons """

        # Actual game keys
        if symbol == key_binds['left']:
            self.left_button_active = True

        elif symbol == key_binds['center']:
            self.middle_button_active = True

        elif symbol == key_binds['right']:
            self.right_button_active = True

    def on_key_release(self, symbol: int, modifiers: int):
        """ This is only for registering if keys are released and to change the relevant buttons """

        # Actual game keys
        if symbol == key_binds['left']:
            self.left_button_active = False

        elif symbol == key_binds['center']:
            self.middle_button_active = False

        elif symbol == key_binds['right']:
            self.right_button_active = False


if __name__ == "__main__":
    window = arcade.Window(GameScreen.width, GameScreen.height, "SETTINGS TEST")
    settings_view = GameScreen()
    settings_view.setup()
    window.show_view(settings_view)
    arcade.run()
