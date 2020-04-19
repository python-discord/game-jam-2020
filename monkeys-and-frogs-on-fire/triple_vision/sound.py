import itertools
from typing import List, Optional

import arcade

from triple_vision.constants import SOUND_FADE_AMOUNT, SOUND_FADE_FREQUENCY


class Sound(arcade.Sound):
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
    def __init__(self, sounds: List[arcade.Sound] = []) -> None:
        self._sounds = sounds
        self._sounds_cycle = itertools.cycle(self._sounds)
        self.curr_sound: Sound = None
        self.tick_delta = 0.0
        self.playing = False

    def add_sound(self, sound: Sound) -> None:
        self._sounds.append(sound)
        self.update_cycle()

    def play_external_sound(
        self, sound_name: str = None, faded: bool = False, max_volume: float = 1.0
    ) -> None:
        self.curr_sound = Sound(sound_name, is_faded=faded, max_volume=max_volume)

    def play_sound_from_list(self, index):
        self.curr_sound = (
            self._sounds[index]
            if index - len(self._sounds) <= index < len(self._sounds)
            else self.curr_sound
        )

    def toggle_next_sound(self) -> None:
        self.curr_sound = next(self._sounds_cycle)

    def update_cycle(self):
        self._sounds_cycle = itertools.cycle(self._sounds)

    @staticmethod
    def load_sound(
        file_name: str, is_faded: bool = False, max_volume: float = 1.0
    ) -> Optional[Sound]:

        try:
            sound = Sound(file_name, is_faded=is_faded, max_volume=max_volume)
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

        if self.tick_delta < SOUND_FADE_FREQUENCY:
            return

        self.curr_sound.set_volume(self.curr_sound.get_volume() + SOUND_FADE_AMOUNT)
