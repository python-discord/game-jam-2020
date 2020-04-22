import random

from triple_vision import Settings as s
from triple_vision.entities import AnimatedEntity


class Spike(AnimatedEntity):

    def __init__(self, view, **kwargs) -> None:
        super().__init__(
            sprite_name='floor_spikes',
            assets_path='assets/dungeon/frames',
            states=('',),
            frame_range=(0, 1, 2, 3, 2, 1, 0),
            **kwargs
        )
        self.camera = view.camera

        self.dmg = random.randrange(40, 50)
        self.throwback_force = 5

        self.ticks = 7
        self.wait_time = random.randrange(2, 10)
        self.waited_time = 0

    def on_update(self, delta_time: float = 1/60) -> None:
        if self.ticks == 7:

            if (
                self.camera.viewport_left < self.center_x < self.camera.viewport_left + s.WINDOW_SIZE[0] and
                self.camera.viewport_bottom < self.center_y < self.camera.viewport_bottom + s.WINDOW_SIZE[1]
            ):

                self.waited_time += delta_time

                if self.waited_time >= self.wait_time:
                    self.ticks = 0
                    self.wait_time = random.randrange(2, 10)
                    self.waited_time = 0

        else:
            if self._prev_anim_delta + delta_time > 0.15:
                self.ticks += 1

            super().on_update(delta_time)

    def play_activate_sound(self) -> None:
        pass

    def play_hit_sound(self) -> None:
        pass
