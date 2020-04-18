import random

import arcade

from triple_vision.entities.sprites import TemporarySprite, MovingSprite


class Weapon(arcade.Sprite):
    def __init__(self, dmg: int, throwback_force: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dmg = dmg
        self.throwback_force = throwback_force


class Projectile(Weapon, TemporarySprite, MovingSprite):
    pass


class LaserProjectile(Projectile):

    def __init__(self, center_x: int, center_y: int, *args, **kwargs):
        super().__init__(
            dmg=random.randrange(60, 70),
            throwback_force=8,
            lifetime=3,
            moving_speed=5,
            filename=":resources:images/space_shooter/laserBlue01.png",
            center_x=center_x,
            center_y=center_y,
            *args,
            **kwargs
        )
