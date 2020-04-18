import enum
import math
from pathlib import Path

import arcade

from triple_vision.entities.entity import AnimatedEntity


class Enemies(enum.Enum):
    big_demon = 0


class BaseEnemy(AnimatedEntity):
    """
    Sprite with idle and run animation.
    """
    enemy_assets_path = Path('assets/dungeon/frames')

    def __init__(self, enemy: Enemies, **kwargs) -> None:
        super().__init__(
            sprite_name=enemy.name,
            assets_path=self.enemy_assets_path,
            **kwargs
        )


class ChasingEnemy(BaseEnemy):
    """
    Simple chasing enemy that tries to catch some other sprite.
    No path-finding, just goes straight to sprite if it is in radius.
    """

    def __init__(
        self,
        enemy: Enemies,
        target_sprite: arcade.Sprite,
        chase_speed: int,
        detection_radius: int,
        **kwargs
    ):
        super().__init__(enemy, **kwargs)
        self.chase_speed = chase_speed
        self.target_sprite = target_sprite
        self.detection_radius = detection_radius

    def _detect(self) -> bool:
        return (
            abs(self.center_x - self.target_sprite.center_x) <= self.detection_radius and
            abs(self.center_y - self.target_sprite.center_y) <= self.detection_radius
        )

    def update(self, delta_time: float = 1/60):
        if self._detect():
            dest_x = self.target_sprite.center_x
            dest_y = self.target_sprite.center_y

            x_diff = dest_x - self.center_x
            y_diff = dest_y - self.center_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * self.chase_speed
            self.change_y = math.sin(angle) * self.chase_speed

        else:
            self.change_x = 0
            self.change_y = 0

        super().update()
