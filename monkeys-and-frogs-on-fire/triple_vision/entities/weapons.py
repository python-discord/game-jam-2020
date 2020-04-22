import random
from typing import Any

from triple_vision.entities.entities import SoundEntity
from triple_vision.entities.sprites import MovingSprite, TemporarySprite


class Weapon(SoundEntity):
    def __init__(
            self,
            dmg: float,
            throwback_force: int,
            activate_sounds: tuple,
            hit_sounds: tuple,
            **kwargs: Any
    ) -> None:
        super().__init__(activate_sounds=activate_sounds, hit_sounds=hit_sounds, **kwargs)
        self.dmg = dmg
        self.throwback_force = throwback_force


class Projectile(Weapon, TemporarySprite, MovingSprite):
    pass


class LaserProjectile(Projectile):
    activate_sounds = ("laser_activate_0.mp3",)
    hit_sounds = ("laser_hit_0.ogg",)

    def __init__(
        self,
        center_x: float,
        center_y: float,
        dmg: float = random.randrange(60, 70),
        moving_speed: float = 5.0,
        **kwargs: Any
    ) -> None:
        super().__init__(
            dmg=dmg,
            throwback_force=8,
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds,
            lifetime=3,
            moving_speed=moving_speed,
            filename='assets/lasers/blue_laser.png',
            center_x=center_x,
            center_y=center_y,
            **kwargs
        )


class Melee(Weapon):
    activate_sounds = ("melee_activate_0.wav", "melee_activate_1.wav", "melee_activate_2.wav")
    hit_sounds = ("melee_hit_0.flac", "melee_hit_1.flac", "melee_hit_2.flac")

    def __init__(self, dmg: float, throwback_force: int) -> None:
        super().__init__(
            dmg,
            throwback_force,
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds
        )
