import arcade
import itertools
import json
import time
import os
import vlc
import _thread
from .perspective_objects import ShapeManager
from .display import ColourBlend as cb


TESTING = False
SAMPLING = False

if SAMPLING:
    sample_list = []
    sample_sec = []
    prev = 0


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
    started = False
    thread_end = False

    def __init__(self, main_):
        self.main = main_
        self.settings = self.main.settings
        self.volume = self.main.settings.volume

    @classmethod
    def _setup(cls, _track: dict, _main):
        cls.track = _track

        path = f"{cls.BASE_DIR}/main/tracks/{cls.track['path'].upper()}.{cls.track['type']}"
        cls.player = vlc.MediaPlayer(path)
        cls.player.audio_set_volume(int(round(_main.volume * 100, 0)))

        if not SAMPLING:
            with open(f"{cls.BASE_DIR}/main/tracks/{cls.track['path']}.json", 'r') as file:
                cls.notes = json.load(file)

    @classmethod
    def _play_in_thread(cls):
        if not SAMPLING:
            time.sleep(1.5)
        cls.player.play()
        time.sleep(0.03)
        cls.started = True
        cls.thread_end = True

    @classmethod
    def _play(cls):
        cls.started = False
        _thread.start_new_thread(cls._play_in_thread, ())
        cls.active = True

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
        try:
            return cls.notes[section][frame]
        except:
            return False, False, False


class PauseScreen:
    pause_sprite_list = arcade.SpriteList()
    BASE_DIR = None
    WIDTH = None
    HEIGHT = None

    @classmethod
    def pause_setup(cls, base_dir, width, height):
        cls.BASE_DIR = base_dir
        cls.WIDTH = width
        cls.HEIGHT = height

    @classmethod
    def pause_menu(cls, brightness):
        cls.pause_sprite_list = arcade.SpriteList()
        cls.pause_sprite_list.append(  # Game Paused text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Game-Paused.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 1.25,
                          scale=1))

        cls.pause_sprite_list.append(  # Main Menu text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Main-Menu.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 1.75,
                          scale=1))

        cls.pause_sprite_list.append(  # settings text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Settings.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 2.5,
                          scale=1))

        cls.pause_sprite_list.append(  # settings text
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Press-SPACE-to-unpause.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 4.75,
                          scale=0.75))

        for sprite in cls.pause_sprite_list:
            sprite.alpha = int(255 * brightness)

        return cls.pause_sprite_list


class ScoreScreen:
    score_sprite_list = arcade.SpriteList()
    BASE_DIR = None
    WIDTH = None
    HEIGHT = None

    @classmethod
    def score_setup(cls, base_dir, width, height):
        cls.BASE_DIR = base_dir
        cls.WIDTH = width
        cls.HEIGHT = height

    @classmethod
    def score_menu(cls, brightness, notes_hit, notes_total, score):
        cls.score_sprite_list = arcade.SpriteList()
        cls.score_sprite_list.append(  # Game ended
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Your-score.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 1.25,
                          scale=1))

        cls.score_sprite_list.append(
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Main-Menu.png",
                          center_x=cls.WIDTH / 2,
                          center_y=cls.HEIGHT / 1.75,
                          scale=1))

        cls.score_sprite_list.append(
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Total-score.png",
                          center_x=cls.WIDTH / 2.75,
                          center_y=cls.HEIGHT / 2.5,
                          scale=0.5))

        cls.score_sprite_list.append(
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Total-notes.png",
                          center_x=cls.WIDTH / 2.75,
                          center_y=cls.HEIGHT / 3.25,
                          scale=0.50))

        cls.score_sprite_list.append(
            arcade.Sprite(filename=f"{cls.BASE_DIR}/main/Resources/game_play/Notes-hit.png",
                          center_x=cls.WIDTH / 2.75,
                          center_y=cls.HEIGHT / 4.0,
                          scale=0.50))

        for sprite in cls.score_sprite_list:
            sprite.alpha = int(255 * brightness)

        return cls.score_sprite_list


class GameLogic:
    @classmethod
    def get_points(cls, note_y, key_height):
        delta = note_y - key_height
        if delta in range(-5, 5):
            return 100  # Perfect
        elif delta in range(-20, -5):
            return 50  # Good
        elif delta in range(-50, -20):
            return 20  # OK
        else:
            return -1  # Miss

    @classmethod
    def check_miss(cls, note_y, key_height):
        delta = note_y - key_height
        return delta not in range(-50, 50)

    @classmethod
    def get_data(cls,
                 keys_list: ("pressed keys", list, tuple),
                 key_data: ("Key sprites", list, tuple),
                 notes: ("note objects", list, tuple)):
        total_points, combos, notes_rendered = 0, 0, 0
        for note in notes:
            if note.note_id == -1:
                if keys_list[0]:
                    points = cls.get_points(note.y, key_data[0].height)
                    if points != -1:
                        total_points += points
                        combos += 1
                        notes_rendered += 1
                    else:
                        combos = -1
                else:
                    if cls.check_miss(note.y, key_data[0].height):
                        combos = -1
            elif not note.note_id:
                if keys_list[1]:
                    points = cls.get_points(note.y, key_data[1].height)
                    if points != -1:
                        total_points += points
                        combos += 1
                        notes_rendered += 1
                    else:
                        combos = -1
                else:
                    if cls.check_miss(note.y, key_data[1].height):
                        combos = -1

            elif note.note_id:
                if keys_list[2]:
                    points = cls.get_points(note.y, key_data[2].height)
                    if points != -1:
                        total_points += points
                        combos += 1
                        notes_rendered += 1
                    else:
                        combos = -1
                else:
                    if cls.check_miss(note.y, key_data[2].height):
                        combos = -1
        return total_points, combos, notes_rendered


class GameScreen(arcade.View, PauseScreen, ScoreScreen):
    """ Main audio playing screen. """

    # settings
    no_fail = True  # no matter how many times u miss you're not gonna loose
    BASE_DIR = os.getcwd()
    note_offset = 3.5

    # setup
    key_binds = None
    left_button_active = False
    middle_button_active = False
    right_button_active = False

    paused = started = False
    left = center = right = False   # notes

    background = None
    key_1, key_2, key_3 = None, None, None
    count_down = []
    to_be_rendered = None
    notes_list = []
    ended = False

    # Game Data
    score = 0
    combo = 0
    notes_hit = 0
    notes_total = 0

    def __init__(self, main_):
        super().__init__()
        self.audio = Audio(main_=main_)
        self.main = main_
        self.settings = main_.settings
        self.WIDTH, self.HEIGHT = self.main.window.width, self.main.window.height
        self.background_sprite = arcade.Sprite(
            filename=f"{self.BASE_DIR}/main/Resources/game_play/Notes-Background.png",
            scale=1,
            image_height=self.HEIGHT,
            image_width=self.WIDTH)
        self.score_pic = arcade.Sprite(filename=f"{self.BASE_DIR}/main/Resources/game_play/Score.png",
                                       scale=0.75)
        self.notes_hit_pic = arcade.Sprite(filename=f"{self.BASE_DIR}/main/Resources/game_play/Notes-hit.png",
                                           scale=0.5)
        self.notes_missed_pic = arcade.Sprite(filename=f"{self.BASE_DIR}/main/Resources/game_play/Notes-missed.png",
                                              scale=0.5)
        self.combo_pic = arcade.Sprite(filename=f"{self.BASE_DIR}/main/Resources/game_play/Combo.png",
                                       scale=0.75)
        self.delta_time = 0

    def setup(self, _track, _main):
        """
        This Adds the background image, Keys 1 -> 3 sprites, and countdown sprites,
        this also setups the audio system and gets that ready as well as the pause-
        page and loads key binds.

        :param _track:
        :return:
        """
        track_timings = {
            'track_1': 17,
            'track_2': 16,
            'track_3': 17,
            'track_4': 16,
            'track_5': 17,
        }
        arcade.schedule(self.on_note_change, 1 / track_timings[_track['path']])
        self.audio._setup(_track, _main)
        self.pause_setup(base_dir=self.BASE_DIR, width=self.WIDTH, height=self.HEIGHT)
        self.score_setup(base_dir=self.BASE_DIR, width=self.WIDTH, height=self.HEIGHT)
        self.key_binds = self.settings.key_binds
        self.background = arcade.Sprite(
            filename=f"{self.BASE_DIR}/main/Resources/background.png",
            scale=0.4,
            image_height=self.HEIGHT * 14/5,
            image_width=self.WIDTH)

        self.key_1 = arcade.Sprite(
            filename=f"{self.BASE_DIR}/main/Resources/game_play/note_key.png",
            scale=(self.WIDTH / self.HEIGHT) / (20/3))
        self.key_2 = arcade.Sprite(
            filename=f"{self.BASE_DIR}/main/Resources/game_play/note_key.png",
            scale=(self.WIDTH / self.HEIGHT) / (20/3))
        self.key_3 = arcade.Sprite(
            filename=f"{self.BASE_DIR}/main/Resources/game_play/note_key.png",
            scale=(self.WIDTH / self.HEIGHT) / (20/3))

        self.count_down.append(
            arcade.Sprite(filename=f"{self.BASE_DIR}/main/Resources/game_play/1.png", scale=1))
        self.count_down.append(
            arcade.Sprite(filename=f"{self.BASE_DIR}/main/Resources/game_play/2.png", scale=1))
        self.count_down.append(
            arcade.Sprite(filename=f"{self.BASE_DIR}/main/Resources/game_play/3.png", scale=1))

    def on_note_change(self, td):
        """ This is the function that cycles through each note array, this is a 3 dimension list,
            Normally this should render at 16 fps to update (on a 4/4 song) This can be 64 fps if
            vlc is being weird?
        """
        if self.audio.thread_end:
            self.audio.active = self.audio.player.is_playing()
        if self.audio.active:
            if not SAMPLING:
                self.left, self.center, self.right = self.audio.get_notes(next(self.audio.frame_count))

                if TESTING:
                    self.left_button_active = self.left
                    self.middle_button_active = self.center
                    self.right_button_active = self.right
                else:
                    if self.left:
                        self.notes_total += 1
                        self.notes_list.append(ShapeManager.create_shape(-1, screen_width=self.WIDTH))
                    if self.center:
                        self.notes_total += 1
                        self.notes_list.append(ShapeManager.create_shape(0, screen_width=self.WIDTH))
                    if self.right:
                        self.notes_total += 1
                        self.notes_list.append(ShapeManager.create_shape(1, screen_width=self.WIDTH))

            else:
                global sample_sec, sample_list, prev
                section, frame = divmod(next(self.audio.frame_count), 16)
                if section != prev:
                    sample_list.append(sample_sec)
                    sample_sec = []
                    prev = section
                sample_sec.append((self.left_button_active, self.middle_button_active, self.right_button_active))

    def on_start(self):
        """ On game start """
        self.started = True
        self.audio._play()
        time.sleep(0.03)

    def on_pause(self):
        """ On game pause """
        self.paused = not self.paused
        self.audio._pause()

    def on_end(self):
        """ On game end """
        if SAMPLING:
            with open('track_1.json', 'w+') as file:
                json.dump(sample_list, file, indent=4)

    def on_update(self, delta_time: float):
        """ In charge of registering if a user had hit or missed a note. """

        self.delta_time = delta_time
        if self.started and not self.paused:  # todo not fuck this
            points_to_add, combos, notes_passed = GameLogic.get_data(
                (self.left_button_active, self.middle_button_active, self.right_button_active),
                (self.key_1, self.key_2, self.key_3),
                self.notes_list
            )
            self.score += points_to_add
            self.notes_hit += notes_passed
            self.combo = (self.combo + combos) if combos != -1 else 0

        if not self.audio.player.is_playing() and \
                self.started and \
                self.audio.started and not\
                self.paused and \
                self.audio.thread_end:
            self.ended = True

    def on_draw(self, time_delta=None, count_down=None):
        """ In charge of rendering the notes at current time. """
        arcade.start_render()
        alpha = int(255 * self.main.brightness)

        # Background rendering
        self.background.center_x = self.WIDTH / 2
        self.background.center_y = self.HEIGHT / 2
        self.background.scale = 0.4
        self.background.width = self.WIDTH
        self.background.alpha = int(200*self.main.brightness)
        self.background.draw()

        # White mask note box
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
        self.background_sprite.alpha = int(255*self.main.brightness)
        self.background_sprite.draw()

        # notes
        if not self.paused and self.started:
            ShapeManager.manage_shapes(self.notes_list, self.main.brightness, speed=256/(1.5/self.delta_time))

        # White box behind the keys
        arcade.draw_rectangle_filled(
            self.WIDTH / 2,
            self.HEIGHT / 10,
            width=self.WIDTH / 2,
            height=self.key_1.height,
            color=cb.brightness(arcade.color.WHITE, self.main.brightness))

        # Renders pressed keys if NOT paused
        if not self.paused and self.started:
            if self.left_button_active:
                self.key_1.center_x = self.WIDTH / 2 - (self.WIDTH / (200 / 30))
                self.key_1.center_y = self.HEIGHT / 10
                self.key_1.scale = ((self.WIDTH / self.HEIGHT) / (20 / 3)) * (self.HEIGHT / 600)
                self.key_1.alpha = int(255*self.main.brightness)
                self.key_1.draw()

            if self.middle_button_active:
                self.key_2.center_x = self.WIDTH / 2
                self.key_2.center_y = self.HEIGHT / 10
                self.key_2.scale = ((self.WIDTH / self.HEIGHT) / (20 / 3)) * (self.HEIGHT / 600)
                self.key_2.alpha = int(255 * self.main.brightness)
                self.key_2.draw()

            if self.right_button_active:
                self.key_3.center_x = self.WIDTH / 2 + (self.WIDTH / (200 / 30))
                self.key_3.center_y = self.HEIGHT / 10
                self.key_3.scale = ((self.WIDTH / self.HEIGHT) / (20 / 3)) * (self.HEIGHT / 600)
                self.key_3.alpha = int(255 * self.main.brightness)
                self.key_3.draw()

        # Audio progress bar
        pos = self.audio.player.get_position()
        lower_x, lower_y = self.WIDTH / 1.1 + self.WIDTH / 150, self.HEIGHT / 20
        height, width = self.HEIGHT - self.HEIGHT / 7, self.WIDTH / 18
        #  todo  add progress bar

        # Labels
        self.score_pic.center_x = self.combo_pic.center_x = self.notes_hit_pic.center_x \
            = self.notes_missed_pic.center_x = (self.WIDTH / 7.5)
        self.score_pic.center_y, self.combo_pic.center_y,\
        self.notes_hit_pic.center_y, self.notes_missed_pic.center_y = \
            (self.HEIGHT / 2) + ((self.HEIGHT / 10) * 1.5), (self.HEIGHT / 2) + ((self.HEIGHT / 10) * 3),\
            (self.HEIGHT / 2) + ((self.HEIGHT / 10) * -1), (self.HEIGHT / 2) + ((self.HEIGHT / 10) * -2.5),

        self.score_pic.alpha = alpha
        self.score_pic.draw()
        self.notes_hit_pic.alpha = alpha
        self.notes_hit_pic.draw()

        # Actual score
        arcade.draw_text(f"{self.score}",
                         start_x=self.score_pic.center_x - (len(f"{self.score}") * 15),
                         start_y=((self.HEIGHT / 2) + ((self.HEIGHT / 10) * 0.35)),
                         color=cb.brightness(arcade.color.WHITE, self.main.brightness),
                         align="center", font_size=50)

        # Actual total hits
        arcade.draw_text(f"{self.notes_hit}",
                         start_x=self.notes_hit_pic.center_x - (len(f"{self.notes_hit}") * 15),
                         start_y=((self.HEIGHT / 2) + ((self.HEIGHT / 10) * -2)),
                         color=cb.brightness(arcade.color.WHITE, self.main.brightness),
                         align="center", font_size=50)

        if self.paused:
            self.background.alpha = 255
            self.background.draw()
            self.pause_menu(self.main.brightness).draw()

        if self.ended:
            self.on_end()
            self.background.alpha = 255
            self.background.draw()
            self.score_menu(self.main.brightness, self.notes_hit, self.notes_total, self.score).draw()

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
