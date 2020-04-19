import itertools
from typing import List

import arcade

from triple_vision.constants import SOUND_FADE_AMOUNT, SOUND_FADE_FREQUENCY


class Sound(arcade.Sound):
    def __init__(
        self,
        *args,
        is_faded: bool = False,
        max_volume: float = 1.0,
        **kwargs
    ) -> None:

        self.faded = is_faded
        self.max_volume = max_volume
        super().__init__(*args, **kwargs)

    def set_volume(self, volume):
        if volume > self.max_volume:
            return
        super().set_volume(volume)


class SoundManager:
    def __init__(self, sounds: List[arcade.Sound]) -> None:
        self._sounds = sounds
        self._sounds_cycle = itertools.cycle(self._sounds)
        self.curr_sound: Sound = None
        self.tick_delta = 0.0
        self.playing = False

    def add_sound(self) -> None:
        pass

    def play_sound(self, index: int = None, sound: arcade.Sound = None) -> None:
        if sound:
            self.curr_sound = sound
        elif index is not None:
            self.curr_sound = self._sounds[index] if index - len(self._sounds) <= index < len(self._sounds) else None
        else:
            raise Exception("Not passed songs to play, aborting.")

    def toggle_next_sound(self) -> None:
        self.curr_sound = next(self._sounds_cycle)

    def on_update(self, delta_time: float) -> None:
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

