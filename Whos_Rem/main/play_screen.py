import arcade
import itertools
import json
import time
import os
import vlc


class Audio:
    BASE_DIR = os.getcwd()
    FPS = 16

    settings = None
    volume = None

    track = None
    music = None
    notes = []
    frame_count = itertools.count(1, 1)
    active = False
    vlc_instance = None
    player = None

    def __init__(self, main_):
        self.main = main_
        self.settings = self.main.settings
        self.volume = self.volume * 0.1

    @classmethod
    def _setup(cls, _track: dict):
        cls.track = _track

        path = f"{cls.BASE_DIR}/tracks/{cls.track['path'].upper()}.{cls.track['type']}"
        cls.vlc_instance = vlc.Instance('--input-repeat=-1')
        cls.player = cls.vlc_instance.media_player_new()
        media = cls.vlc_instance.media_new(path)
        cls.player.set_media(media)

        with open(f"{cls.BASE_DIR}/tracks/{cls.track['path']}.json", 'r') as file:
            cls.notes = json.load(file)

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


class PauseScreen:
    sprite_list = arcade.SpriteList()
    BASE_DIR = None
    WIDTH = None
    HEIGHT = None

    @classmethod
    def pause_setup(cls, base_dir, width, height):
        cls.BASE_DIR = base_dir
        cls.WIDTH = width
        cls.HEIGHT = height

    @classmethod
    def pause_menu(cls):
        cls.sprite_list.append(  # Game Paused text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/Resources/game_play/Game-Paused.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 1.25,
                          scale=1))

        cls.sprite_list.append(  # Main Menu text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/Resources/game_play/Main-Menu.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 1.75,
                          scale=1))

        cls.sprite_list.append(  # settings text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/Resources/game_play/Settings.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 2.5,
                          scale=1))

        cls.sprite_list.append(  # settings text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/Resources/game_play/Press-SPACE-to-unpause.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 4.75,
                          scale=0.75))

        return cls.sprite_list


class GameScreen(arcade.View, PauseScreen):
    """ Main audio playing screen. """

    # settings
    no_fail = True  # no matter how many times u miss you're not gonna loose
    BASE_DIR = os.getcwd()

    # setup
    key_binds = None
    left_button_active = False
    middle_button_active = False
    right_button_active = False

    paused = started = False
    left = center = right = False   # notes

    background = None
    note_1, note_2, note_3 = None, None, None
    count_down = []
    to_be_rendered = None

    def __init__(self, main_):
        super().__init__()
        self.audio = Audio(main_=main_)
        self.main = main_
        self.settings = main_.settings
        self.background_sprite = arcade.Sprite(
            filename=f"{self.BASE_DIR}/Resources/game_play/Notes-Background.png",
            scale=1,
            image_height=self.HEIGHT,
            image_width=self.WIDTH)

    def setup(self, _track):
        arcade.schedule(self.on_note_change, 1 / 16)
        self.audio._setup(_track)
        self.pause_setup(base_dir=self.BASE_DIR, width=self.WIDTH, height=self.HEIGHT)
        self.key_binds = self.settings.key_binds
        self.background = arcade.Sprite(
            filename=f"{self.BASE_DIR}/Resources/background.png",
            scale=0.4,
            image_height=self.HEIGHT * 14/5,
            image_width=self.WIDTH)

        self.note_1 = arcade.Sprite(
            filename=f"{self.BASE_DIR}/Resources/game_play/note_key.png",
            scale=(self.WIDTH / self.HEIGHT) / (20/3))
        self.note_2 = arcade.Sprite(
            filename=f"{self.BASE_DIR}/Resources/game_play/note_key.png",
            scale=(self.WIDTH / self.HEIGHT) / (20/3))
        self.note_3 = arcade.Sprite(
            filename=f"{self.BASE_DIR}/Resources/game_play/note_key.png",
            scale=(self.WIDTH / self.HEIGHT) / (20/3))

        self.count_down.append(
            arcade.Sprite(filename=f"{self.BASE_DIR}/Resources/game_play/1.png", scale=1))
        self.count_down.append(
            arcade.Sprite(filename=f"{self.BASE_DIR}/Resources/game_play/2.png", scale=1))
        self.count_down.append(
            arcade.Sprite(filename=f"{self.BASE_DIR}/Resources/game_play/3.png", scale=1))

    @staticmethod
    def draw_note_key(x, y, height, width):
        arcade.draw_rectangle_filled(x, y, width=width, height=height, color=arcade.color.CRIMSON)

    def on_note_change(self, td):
        self.active = self.audio.player.is_playing()
        if self.active:
            self.left, self.center, self.right = self.audio.get_notes(next(self.audio.frame_count))

        elif not self.paused and not self.active and self.started:
            pass
            # with open(f"{self.BASE_DIR}/tracks/{self.track['path']}_new.json", 'w+') as file:
            #   json.dump(self.notes_, file)

    def on_start(self):
        self.started = True
        self.audio._play()

    def on_pause(self):
        self.paused = not self.paused
        #if not self.paused: todo fix?
        #    for i in range(3):  # 3 sec time
        #        self.to_be_rendered = self.count_down[i]
        self.audio._pause()

    def on_update(self, delta_time: float):
        """ In charge of registering if a user had hit or missed a note. """
        pass

    def on_draw(self, time_delta=None, count_down=None):
        """ In charge of rendering the notes at current time. """
        arcade.start_render()

        # Background rendering
        self.background.center_x = self.WIDTH / 2
        self.background.center_y = self.HEIGHT / 2
        self.background.scale = 0.4
        self.background.width = self.WIDTH
        self.background.alpha = 200
        self.background.draw()

        # White key note box
        arcade.draw_rectangle_filled(
            self.WIDTH / 2,
            self.HEIGHT / 2,
            width=self.WIDTH / 2,
            height=self.HEIGHT,
            color=arcade.color.WHITE)

        # Note background sprite render
        self.background_sprite.center_x = self.WIDTH / 2
        self.background_sprite.center_y = self.HEIGHT / 2
        self.background_sprite.scale = 1
        self.background_sprite.width = self.WIDTH / 2
        self.background_sprite.alpha = 160
        self.background_sprite.draw()

        # If un pausing render
        if count_down is not None:
            count_down.draw()

        # Honestly no idea what this was but probably important
        arcade.draw_rectangle_filled(
            self.WIDTH / 2,
            self.HEIGHT / 10,
            width=self.WIDTH / 2,
            height=self.HEIGHT / 4,
            color=arcade.color.WHITE)

        # Renders pressed keys if NOT paused
        if not self.paused and self.started:
            if self.left_button_active:
                self.note_1.center_x = self.WIDTH / 2 - 105
                self.note_1.center_y = self.HEIGHT / 10
                self.note_1.draw()

            if self.middle_button_active:
                self.note_2.center_x = self.WIDTH / 2
                self.note_2.center_y = self.HEIGHT / 10
                self.note_2.draw()

            if self.right_button_active:
                self.note_3.center_x = self.WIDTH / 2 + 105
                self.note_3.center_y = self.HEIGHT / 10
                self.note_3.draw()

        # Audio progress bar
        pos = self.audio.player.get_position()
        lower_x, lower_y = self.WIDTH / 1.1 + self.WIDTH / 150, self.HEIGHT / 20
        height, width = self.HEIGHT - self.HEIGHT / 7, self.WIDTH / 18

        # Black outline
        arcade.draw_line(start_x=lower_x,
                         start_y=lower_y,
                         end_x=lower_x + 300,
                         end_y=height,
                         line_width=width,
                         color=arcade.color.CRIMSON)
        # Filled
        arcade.draw_line(start_x=lower_x + 5,
                         start_y=lower_y,
                         end_x=lower_x + 300 - 5,
                         end_y=height * pos,
                         line_width=width,
                         color=arcade.color.CRIMSON)

        # Shows Pause menu because i suck?
        if self.paused:
            self.background.alpha = 255
            self.background.draw()
            self.pause_menu().draw()

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



