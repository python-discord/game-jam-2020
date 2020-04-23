import random
from typing import Tuple

from triple_vision import Settings as s
from triple_vision.entities import (
    AnimatedEntity,
    BaseEnemy,
    Player,
    SoundEntity
)
from triple_vision.utils import is_in_radius


class Trap(AnimatedEntity, SoundEntity):
    def __init__(
            self,
            dmg: float,
            throwback_force: int,
            target_player: Player,
            target_enemies: BaseEnemy,
            activation_rectangle: Tuple[int, int, int, int],
            working_radius: int = s.WINDOW_SIZE[0],
            sound_radius: int = s.WINDOW_SIZE[0]//5,
            **kwargs
    ):
        super().__init__(
            assets_path='assets/dungeon/frames',
            states=('',),
            **kwargs
        )
        self.dmg = dmg
        self.throwback_force = throwback_force
        self.target_player = target_player
        self.target_enemies = target_enemies
        self.working_radius = working_radius
        self.activation_rectangle = activation_rectangle
        self.sound_radius = sound_radius

    def is_activated(self):
        """
        Should the trap work aka should it be animated and play sounds,
        Good for saving resources if trap is off screen or far for player.
        """
        return is_in_radius(self, self.target_player, self.working_radius)

    def will_activate(self):
        """
        Based on self.target_player and self.activation_rectangle.
        activation_rectangle is x_left, y_down, x_right, y_up relative area to self
        where the trap will activate if the player is in that area
        """
        pass

    def activate(self):
        # To be overwritten
        pass

    def play_activate_sound(self) -> None:
        if self.is_in_sound_radius():
            super().play_activate_sound()

    def is_in_sound_radius(self):
        """
        Whether should we play sound effects (activation etc) or not.
        Reduced sound spam.
        """
        return is_in_radius(self, self.target_player, self.sound_radius)


class Spike(Trap):
    # TODO change these assets
    activate_sounds = ("melee_activate_0.wav",)
    hit_sounds = ("melee_hit_0.flac",)

    def __init__(self, target_player=None, target_enemies=None, **kwargs) -> None:
        super().__init__(
            dmg=random.randrange(40, 50),
            throwback_force=5,
            target_player=target_player,
            target_enemies=target_enemies,
            activation_rectangle=(-10, -10, 10, 10),
            sprite_name='floor_spikes',
            frame_range=(0, 1, 2, 3, 2, 1, 0),
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds,
            **kwargs
        )
        self.ticks = 7
        self.wait_time = random.randrange(2, 10)
        self.waited_time = 0

    def on_update(self, delta_time: float = 1/60) -> None:
        if self.ticks == 7:

            if self.is_activated():
                self.waited_time += delta_time

                if self.waited_time >= self.wait_time:
                    self.ticks = 0
                    self.wait_time = random.randrange(2, 10)
                    self.waited_time = 0
        else:
            if self._prev_anim_delta + delta_time > 0.15:
                self.play_activate_sound()
                self.ticks += 1

            super().on_update(delta_time)

    def activate(self):
        # TODO
        pass
