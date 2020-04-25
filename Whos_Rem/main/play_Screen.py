import arcade
import itertools
import json
import time
import os
import vlc
from screeninfo import get_monitors
from Settings import Settings


class Audio:
    BASE_DIR = os.getcwd()
    WIDTH = 1000  # get_monitors()[0].width
    HEIGHT = 600  # get_monitors()[0].height
    FPS = 16

    settings = Settings()
    volume = settings.volume * 0.1

    track = None
    music = None
    notes = []
    frame_count = itertools.count(1, 1)
    background_sprite = None
    active = False
    vlc_instance = None
    player = None

    @classmethod
    def _setup(cls, _track: dict):
        cls.track = track

        path = f"{cls.BASE_DIR}/tracks/{cls.track['path'].upper()}.{cls.track['type']}"
        cls.vlc_instance = vlc.Instance('--input-repeat=-1')
        cls.player = cls.vlc_instance.media_player_new()
        media = cls.vlc_instance.media_new(path)
        cls.player.set_media(media)

        with open(f"{cls.BASE_DIR}/tracks/{cls.track['path']}.json", 'r') as file:
            cls.notes = json.load(file)

        cls.background_sprite = arcade.Sprite(
            filename=f"{cls.BASE_DIR}/Resources/game_play/Notes-Background.png",
            scale=1,
            image_height=cls.HEIGHT,
            image_width=cls.WIDTH)

    @classmethod
    def _play(cls):
        cls.player.play()
        cls.active = True
        time.sleep(0.01)

    @classmethod
    def _pause(cls):
        cls.player.pause()
        cls.active = False

    @classmethod
    def _stop(cls):
        cls.player.stop()
        cls.active = False

    @classmethod
    def get_notes(cls, frame):
        section, frame = divmod(frame, cls.FPS)
        return cls.notes[section][frame]


class GameScreen(arcade.View, Audio):
    """ Main audio playing screen. """

    # settings
    no_fail = True  # no matter how many times u miss you're not gonna loose

    # setup
    key_binds = None
    left_button_active = False
    middle_button_active = False
    right_button_active = False

    paused = started = False
    left = center = right = False   # notes

    background = None
    sprite_list = arcade.SpriteList()

    def setup(self, _track):
        arcade.schedule(self.on_note_change, 1 / 16)
        self._setup(_track)
        self.key_binds = self.settings.key_binds
        self.background = arcade.Sprite(
            filename=f"{self.BASE_DIR}/Resources/background.png",
            scale=0.4,
            image_height=self.HEIGHT * 14/5,
            image_width=self.WIDTH)

    @staticmethod
    def draw_note_key(x, y, height, width):
        arcade.draw_rectangle_filled(x, y, width=width, height=height, color=arcade.color.CRIMSON)

    def on_note_change(self, td):
        self.active = self.player.is_playing()
        if self.active:
            self.left, self.center, self.right = self.get_notes(next(self.frame_count))

        elif not self.paused and not self.active and self.started:
            pass
            # with open(f"{self.BASE_DIR}/tracks/{self.track['path']}_new.json", 'w+') as file:
            #   json.dump(self.notes_, file)

    def on_start(self):
        self.started = True
        self._play()

    def on_pause(self):
        self.paused = not self.paused
        self._pause()

    def on_update(self, delta_time: float):
        """ In charge of registering if a user had hit or missed a note. """
        pass

    def on_draw(self, time_delta=None):
        """ In charge of rendering the notes at current time. """
        arcade.start_render()
        self.background.center_x = self.WIDTH / 2
        self.background.center_y = self.HEIGHT / 2
        self.background.scale = 0.4
        self.background.width = self.WIDTH
        self.background.alpha = 200
        self.background.draw()

        arcade.draw_rectangle_filled(
            self.WIDTH / 2,
            self.HEIGHT / 2,
            width=self.WIDTH / 2,
            height=self.HEIGHT,
            color=arcade.color.WHITE)
        self.background_sprite.center_x = self.WIDTH / 2
        self.background_sprite.center_y = self.HEIGHT / 2
        self.background_sprite.scale = 1
        self.background_sprite.width = self.WIDTH / 2
        self.background_sprite.alpha = 160
        self.background_sprite.draw()

        arcade.draw_rectangle_filled(
            self.WIDTH / 2,
            self.HEIGHT / 10,
            width=self.WIDTH / 2,
            height=self.HEIGHT / 4,
            color=arcade.color.WHITE)

        if not self.paused and self.started:
            if self.left_button_active:
                self.draw_note_key(self.WIDTH / 2 - 105, self.HEIGHT / 10, self.HEIGHT / 4, self.WIDTH / 10)

            if self.middle_button_active:
                self.draw_note_key(self.WIDTH / 2, self.HEIGHT / 10, self.HEIGHT / 4, self.WIDTH / 10)

            if self.right_button_active:
                self.draw_note_key(self.WIDTH / 2 + 105, self.HEIGHT / 10, self.HEIGHT / 4, self.WIDTH / 10)

        if self.paused:
            self.background.alpha = 255
            self.background.draw()
            self.sprite_list.append(    # Game Paused text
                arcade.Sprite(filename=f"{self.BASE_DIR}/Resources/game_play/Game-Paused.png",
                              center_x=self.WIDTH / 2,
                              center_y=self.HEIGHT / 1.25,
                              scale=1))

            self.sprite_list.append(  # Main Menu text
                arcade.Sprite(filename=f"{self.BASE_DIR}/Resources/game_play/Main-Menu.png",
                              center_x=self.WIDTH / 2,
                              center_y=self.HEIGHT / 1.75,
                              scale=1))

            self.sprite_list.append(  # settings text
                arcade.Sprite(filename=f"{self.BASE_DIR}/Resources/game_play/Settings.png",
                              center_x=self.WIDTH / 2,
                              center_y=self.HEIGHT / 2.5,
                              scale=1))

            self.sprite_list.append(  # settings text
                arcade.Sprite(filename=f"{self.BASE_DIR}/Resources/game_play/Press-SPACE-to-unpause.png",
                              center_x=self.WIDTH / 2,
                              center_y=self.HEIGHT / 4.75,
                              scale=0.75))

            self.sprite_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """ This is only for registering if keys are pressed and to change the relevant buttons """

        # Actual game keys
        if symbol == self.key_binds['left']:
            self.left_button_active = True

        elif symbol == self.key_binds['center']:
            self.middle_button_active = True

        elif symbol == self.key_binds['right']:
            self.right_button_active = True

        elif symbol == arcade.key.SPACE:
            if not self.started:
                self.on_start()
            else:
                self.on_pause()

    def on_key_release(self, symbol: int, modifiers: int):
        """ This is only for registering if keys are released and to change the relevant buttons """

        # Actual game keys
        if symbol == self.key_binds['left']:
            self.left_button_active = False

        elif symbol == self.key_binds['center']:
            self.middle_button_active = False

        elif symbol == self.key_binds['right']:
            self.right_button_active = False


if __name__ == '__main__':
    track = {'path': 'track_1',
             'type': 'wav',
             'name': 'undertale'}

    game = GameScreen()
    game.setup(_track=track)

    window = arcade.Window(GameScreen.WIDTH, GameScreen.HEIGHT, "SETTINGS TEST")
    window.show_view(game)
    arcade.run()
