import random
from typing import Any

import arcade

from triple_vision.entities.sprites import TemporarySprite, MovingSprite


class Weapon(arcade.Sprite):
    def __init__(self, dmg: float, throwback_force: int, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.dmg = dmg
        self.throwback_force = throwback_force


class Projectile(Weapon, TemporarySprite, MovingSprite):
    pass


class LaserProjectile(Projectile):

    def __init__(
        self,
        center_x: float,
        center_y: float,
        *args: Any,
        dmg: float = random.randrange(60, 70),
        moving_speed: float = 5.0,
        **kwargs: Any
    ) -> None:
        super().__init__(
            dmg=dmg,
            throwback_force=8,
            lifetime=3,
            moving_speed=moving_speed,
            filename='assets/lasers/blue_laser.png',
            center_x=center_x,
            center_y=center_y,
            *args,
            **kwargs
        )
