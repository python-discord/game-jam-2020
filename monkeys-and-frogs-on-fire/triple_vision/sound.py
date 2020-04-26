import itertools
from pathlib import Path
from typing import List, Optional

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
    def __init__(self, sounds: List[arcade.Sound] = []) -> None:
        self._volume = ss.DEFAULT_VOLUME
        self._sounds = sounds
        self._sounds_cycle = itertools.cycle(self._sounds)
        self.curr_sound: SoundTrack = None
        self.tick_delta = 0.0
        self.playing = False

    def add_sound(self, sound_name: str, faded: bool = False, max_volume: float = 1.0) -> None:
        self._sounds.append(SoundTrack(sound_name, is_faded=faded, max_volume=max_volume))
        self.update_cycle()

    def remove_sound(self, sound_name: str):
        self._sounds = [sound for sound in self._sounds if sound.file_name != sound_name]
        self.update_cycle()

    def play_external_sound(
        self, sound_name: str = None, faded: bool = False, max_volume: float = 1.0
    ) -> None:
        self.curr_sound = SoundTrack(sound_name, is_faded=faded, max_volume=max_volume)
        self.playing = False

    def play_sound_from_list(self, index):
        self.curr_sound = (
            self._sounds[index]
            if index - len(self._sounds) <= index < len(self._sounds)
            else self.curr_sound
        )
        self.playing = False

    def toggle_next_sound(self) -> None:
        self.curr_sound = next(self._sounds_cycle)
        self.playing = False

    def update_cycle(self):
        self._sounds_cycle = itertools.cycle(self._sounds)

    @staticmethod
    def load_sound(
        file_name: str, is_faded: bool = False, max_volume: float = 1.0
    ) -> Optional[SoundTrack]:

        try:
            sound = SoundTrack(file_name, is_faded=is_faded, max_volume=max_volume)
            return sound
        except Exception as e:
            print(f'Unable to load sound file: "{file_name}". Exception: {e}')
            return None

    def update(self, delta_time: float) -> None:
        self.tick_delta += delta_time

        if self.curr_sound is None:
            return

        if not self.playing:
            arcade.play_sound(self.curr_sound)
            self.playing = True

        if not self.curr_sound.faded:
            return

        if self.tick_delta < ss.FADE_FREQUENCY:
            return
        print(self.curr_sound.get_volume() + ss.FADE_AMOUNT)
        self.curr_sound.set_volume(self.curr_sound.get_volume() + ss.FADE_AMOUNT)
        self.tick_delta = 0.0
