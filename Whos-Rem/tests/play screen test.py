import arcade
from screeninfo import get_monitors
import pyaudio
import aubio

song_filepath = r"F:\game-jam-2020\Whos-Rem\Audio-Managment\test-clips\Camellia_MEGALOVANIA_Remix.wav"
win_s = 1024                # fft size
hop_s = win_s // 2          # hop size

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
    frame_counter = 0
    paused = started = False
    all_sprites_list = arcade.SpriteList()
    background_sprite = arcade.Sprite(
        filename=r"F:\game-jam-2020\Whos-Rem\main\reasources\game_play\undertale.png",
        scale=1,
        image_height=height,
        image_width=width,
    )

    # Audio side of stuff

    # settings
    no_fail = True  # no matter how many times u miss you're not gonna loose
    fps = 32    # used for calculations
    song = arcade.Sound(song_filepath, streaming=True)

    def setup(self):
        arcade.schedule(self.on_frame_draw, 1 / 32)
        self.song.play(0.05)

    def on_update(self, delta_time: float):
        """ In charge of registering if a user had hit or missed a note. """

    def on_frame_draw(self, time_delta):
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

    def on_draw(self):
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
            arcade.draw_rectangle_filled(
                self.width / 2 - 105,
                self.height / 10,
                width=self.width / 10,
                height=self.height / 4,
                color=arcade.color.CRIMSON)

        if self.middle_button_active:
            arcade.draw_rectangle_filled(
                self.width / 2,
                self.height / 10,
                width=self.width / 10,
                height=self.height / 4,
                color=arcade.color.CRIMSON)

        if self.right_button_active:
            arcade.draw_rectangle_filled(
                self.width / 2 + 105,
                self.height / 10,
                width=self.width / 10,
                height=self.height / 4,
                color=arcade.color.CRIMSON)

    def on_key_press(self, symbol: int, modifiers: int):
        """ This is only for registering if keys are pressed and to change the relevant buttons """

        # Start key (normally space)
        if symbol == 32:   # todo test this cuz idk what it is
            self.paused = not self.paused   # this toggles the game paused / stopped or not
            if not self.started:
                self.started = True

        # Actual game keys
        elif symbol == key_binds['left']:   # todo test this cuz idk what it is
            self.left_button_active = True

        elif symbol == key_binds['center']:   # todo test this cuz idk what it is
            self.middle_button_active = True

        elif symbol == key_binds['right']:   # todo test this cuz idk what it is
            self.right_button_active = True

    def on_key_release(self, symbol: int, modifiers: int):
        """ This is only for registering if keys are released and to change the relevant buttons """
        # Actual game keys
        if symbol == key_binds['left']:  # todo test this cuz idk what it is
            self.left_button_active = False

        elif symbol == key_binds['center']:  # todo test this cuz idk what it is
            self.middle_button_active = False

        elif symbol == key_binds['right']:  # todo test this cuz idk what it is
            self.right_button_active = False


if __name__ == "__main__":
    window = arcade.Window(GameScreen.width, GameScreen.height, "SETTINGS TEST")
    settings_view = GameScreen()
    settings_view.setup()
    window.show_view(settings_view)
    arcade.run()
