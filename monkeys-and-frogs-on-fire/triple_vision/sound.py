from pathlib import Path

import arcade

from triple_vision import SoundSettings as ss


class SoundTrack(arcade.Sound):
    def __init__(
        self, *args, is_faded: bool = False, max_volume: float = 1.0, **kwargs
    ) -> None:
        self.faded = is_faded
        self.max_volume = max_volume
        super().__init__(*args, **kwargs)

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
            cls.update_volumes(0.1)
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


