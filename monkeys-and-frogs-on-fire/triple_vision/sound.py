import time
from pathlib import Path
from typing import List

import arcade

from triple_vision import SoundSettings as ss


class SoundTrack(arcade.Sound):
    _sound_track_assets_path = Path("./assets/audio/soundtracks")

    def __init__(
        self, file_name, is_faded: bool = False, max_volume: float = 1.0, **kwargs
    ) -> None:
        self.faded = is_faded
        self.max_volume = max_volume
        super().__init__(file_name=str(self._sound_track_assets_path / file_name), **kwargs)

    def set_volume(self, volume):
        if volume > self.max_volume:
            return
        super().set_volume(volume)


class SoundManager:
    _sound_assets_path = Path("./assets/audio/sounds")
    # Keys are sounds path, values are sounds
    _loaded_sounds = {}  # keys are sounds path, values are sound objects
    _volume = ss.DEFAULT_VOLUME
    _tick_delta = 0.0
    _slow_mode_activated = False

    @classmethod
    def add_sound(cls, sound_name: str):
        path = cls.get_sound_path(sound_name)
        if path in cls._loaded_sounds:
            return

        sound = arcade.load_sound(path)
        if sound is not None:
            cls._loaded_sounds[path] = sound

    @classmethod
    def get_sound_path(cls, sound_name: str) -> str:
        return str(cls._sound_assets_path / sound_name)

    @classmethod
    def play_sound(cls, sound_name: str) -> None:
        path = cls.get_sound_path(sound_name)
        if path not in cls._loaded_sounds:
            # TODO Can we just add it automatically?
            print(f"Can't play sound {path} add it first!")
            return

        cls._loaded_sounds[path].play()
        cls._loaded_sounds[path].set_volume(cls._volume)

    @classmethod
    def update(cls, slow_mode: bool = False) -> None:
        if slow_mode:
            cls._slow_mode_activated = True
            cls.update_volumes(0.025)
        elif cls._slow_mode_activated:
            cls._slow_mode_activated = False
            cls.update_volumes(cls._volume)

    @classmethod
    def update_volumes(cls, volume: float):
        for sound in cls._loaded_sounds.values():
            try:
                sound.set_volume(volume)
            except TypeError:
                # We cannot know if the sound is playing or not and
                # set_volume only works if it's playing
                pass


class SoundtrackManager:
    def __init__(self, music_list: List[str]):
        # Variables used to manage our music. See setup() for giving them
        # values.
        self._volume = ss.DEFAULT_VOLUME
        self._sound_assets_path = Path("./assets/audio/soundtracks")
        self.music_list = [self.get_sound_path(file_name) for file_name in music_list]
        self.current_song_position = 0
        self.curr_sound = None

    def get_sound_path(self, sound_name: str) -> str:
        return str(self._sound_assets_path / sound_name)

    def add_sound(self, file_name: str):
        self.music_list.append(self.get_sound_path(file_name))

    def remove_sound(self, file_name: str):
        if file_name not in self.music_list:
            return
        self.music_list.remove(file_name)

    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """
        self.current_song_position += 1
        if self.current_song_position >= len(self.music_list):
            self.current_song_position = 0
        print(f"Advancing song to {self.current_song_position}.")

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.curr_sound:
            self.curr_sound.stop()

        # Play the next song
        print(f"Playing {self.music_list[self.current_song_position]}")
        self.curr_sound = arcade.Sound(self.music_list[self.current_song_position], streaming=True)
        self.curr_sound.play(self._volume)
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Array index of what to play
        self.current_song_position = 0
        # Play the song
        self.play_song()

    def update(self):

        position = self.curr_sound.get_stream_position()

        # The position pointer is reset to 0 right after we finish the song.
        # This makes it very difficult to figure out if we just started playing
        # or if we are doing playing.
        if position == 0.0:
            self.advance_song()
            self.play_song()

    def update_volumes(self, volume: float):
        self._volume = volume
