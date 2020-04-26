import math
import random
from typing import Any

import arcade

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
    def destroy(self):
        self.kill()


class LaserProjectile(Projectile):
    activate_sounds = ("laser_activate_2.wav",)
    hit_sounds = ("laser_hit_1.wav",)

    def __init__(
        self,
        color: str,
        dmg: float = random.randrange(60, 70),
        moving_speed: float = 5.0,
        lifetime: float = 2,
        **kwargs: Any
    ) -> None:
        super().__init__(
            dmg=dmg,
            throwback_force=8,
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds,
            lifetime=lifetime,
            moving_speed=moving_speed,
            filename=f'assets/lasers/{color}_laser.png',
            **kwargs
        )


class ChargedLaserProjectile(Projectile):
    activate_sounds = ("laser_activate_2.wav",)
    hit_sounds = ("laser_hit_1.wav",)

    def __init__(
        self,
        charge: int,
        **kwargs: Any
    ) -> None:
        """
        :param: charge integer from 1-100
        """

        dmg = random.randrange(60 + int(charge), 70 + math.ceil(charge))
        lifetime = 2 - round(charge/60, 2)
        moving_speed = 5.0 + round(charge/10, 2)
        throwback_force = 8 + charge//10

        super().__init__(
            dmg=dmg,
            throwback_force=throwback_force,
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds,
            lifetime=lifetime,
            moving_speed=moving_speed,
            filename='assets/lasers/blue_laser.png',
            **kwargs
        )

        self.scale = 1 + round(charge/100, 2)
        self.alpha = 200 + charge//2


class Melee(Weapon):
    activate_sounds = ("melee_activate_0.wav", "melee_activate_1.wav", "melee_activate_2.wav")
    hit_sounds = ("melee_hit_0.flac", "melee_hit_1.flac", "melee_hit_2.flac")

    def __init__(self, dmg: float, throwback_force: int, **kwargs) -> None:
        super().__init__(
            dmg,
            throwback_force,
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds,
            **kwargs
        )


class FloorStompMelee(Projectile):
    activate_sounds = ("fireball.wav",)
    hit_sounds = ("laser_hit_1.wav",)

    def __init__(
        self,
        center_x: float,
        center_y: float,
        dmg: float = random.randrange(512, 1024),
        moving_speed: float = 0.0,
        **kwargs: Any
    ) -> None:

        super().__init__(
            dmg=dmg,
            throwback_force=8,
            activate_sounds=self.activate_sounds,
            hit_sounds=self.hit_sounds,
            lifetime=0.25,
            moving_speed=moving_speed,
            filename=f':resources:images/pinball/pool_cue_ball.png',
            center_x=center_x,
            center_y=center_y,
            **kwargs
        )
        self.alpha = 0
        self._tick_delta = 0.0
        self.scale = 10  # this one actually kills but is invisible because alpha 0
        # This one is just effect
        self.effect_sprite = arcade.Sprite(
            filename=f':resources:images/pinball/pool_cue_ball.png',
            center_x=center_x,
            center_y=center_y
        )
        self.effect_sprite.alpha = 100
        self.effect_sprite.scale = 5

    def on_update(self, delta_time: float):
        # Remember that this is tied to lifetime, it will keep going until temporal sprite
        # destroys itself
        self._tick_delta += delta_time

        if self._tick_delta > 0.05:
            self.effect_sprite.scale += 1
            self._tick_delta = 0.0

        super().on_update(delta_time)

    def kill(self):
        self.effect_sprite.kill()
        super().kill()
