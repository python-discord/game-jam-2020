import random
from typing import Tuple, List, Union

from triple_vision import Settings as s
from triple_vision.entities import AnimatedEntity, SoundEntity, BaseEnemy, Player


class Trap(AnimatedEntity, SoundEntity):
    def __init__(
            self,
            dmg: float,
            throwback_force: int,
            targets: List[Union[BaseEnemy, Player]],
            working_radius: int,
            activation_rectangle: Tuple[int, int, int, int],
            **kwargs
    ):
        super().__init__(assets_path='assets/dungeon/frames',
                         states=('',),
                         **kwargs)
        self.dmg = dmg
        self.throwback_force = throwback_force
        self.targets = targets
        self.working_radius = working_radius
        self.activation_rectangle = activation_rectangle


class Spike(Trap):
    # TODO change these assets
    activate_sounds = ("fireball.wav",)
    hit_sounds = ("fireball.wav",)

    def __init__(self, view, **kwargs) -> None:
        super().__init__(
            dmg=random.randrange(40, 50),
            throwback_force=5,
            targets=None,
            working_radius=400,
            activation_rectangle=(-10, -10, 10, 10),
            sprite_name='floor_spikes',
            frame_range=(0, 1, 2, 3, 2, 1, 0),
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds,
            **kwargs
        )
        self.camera = view.camera

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
            self.play_activate_sound()
