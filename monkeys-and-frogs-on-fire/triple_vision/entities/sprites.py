import math
import time
from typing import Optional

import arcade

from triple_vision.constants import SCALED_TILE, ON_CARD_HOVER_SLOWDOWN_MULTIPLIER
from triple_vision.utils import get_change_vector


class MovingSprite(arcade.Sprite):
    def __init__(self, moving_speed, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed = moving_speed
        self.speed_multiplier = 1
        self.target = None

    def move_to(self, x: float, y: float, *, rotate: bool = True, set_target: bool = True) -> None:
        """
        Move the MovingSprite into a given point on the screen.

        :param set_target: Represents if we want to set the point as a target
                           (the sprite will stop after reaching it)
        :param x: x coordinate for the sprite to move into
        :param y: y coordinate for the sprite to move into
        :param rotate: represents if we need to rotate the sprite or not
        """

        self.change_x, self.change_y, angle = get_change_vector(
            start_position=self.position,
            destination_position=(x, y),
            speed_multiplier=self.speed * self.speed_multiplier
        )

        if rotate:
            # Angle the sprite
            self.angle = math.degrees(angle)

        if set_target:
            self.target = (x, y)

    def move_to_sprite(
            self,
            sprite: arcade.Sprite,
            *,
            rotate: bool = True,
            set_target: bool = True
    ) -> None:
        self.move_to(sprite.center_x, sprite.center_y, rotate=rotate, set_target=set_target)

    def move_to_angle(self, angle: int, *, rotate: bool = False) -> None:
        """
        Move in direction of angle.
        :param angle: angle in degrees to which to move the sprite (90 means to move sprite up)
        :param rotate: should we rotate the sprite around it's center to align it to the new
                       direction. Useful for example projectiles.
        """
        if rotate:
            self.angle = angle

        radians_angle = math.radians(angle)

        # Taking into account the angle, calculate our change_x and change_y.
        self.change_x = math.cos(radians_angle) * self.speed
        self.change_y = math.sin(radians_angle) * self.speed

    def on_update(self, delta_time: float = 1/60) -> None:
        if self.target is not None:
            if (
                self.target[0] - SCALED_TILE / 2 < self.center_x < self.target[0] + SCALED_TILE / 2 and
                self.target[1] - SCALED_TILE / 2 < self.center_y < self.target[1] + SCALED_TILE / 2
            ):
                self.change_x = 0
                self.change_y = 0

                self.target = None

        self.update_(delta_time)

    def update_(self, delta_time):
        slowdown = delta_time * 60
        self.position = [
            self._position[0] + self.change_x * slowdown,
            self._position[1] + self.change_y * slowdown
        ]
        self.angle += self.change_angle * slowdown


class TemporarySprite(arcade.Sprite):
    def __init__(self, lifetime: Optional[int], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.lifetime = lifetime
        self._passed_time = 0.0
        self.created_at = time.time()

    def on_update(self, delta_time: float):
        self._passed_time += delta_time
        if self.lifetime and self._passed_time > self.lifetime:
            self.kill()
        super().on_update(delta_time)


class DamageIndicator(TemporarySprite, MovingSprite):
    def __init__(self, text, start_x: int, start_y: int):
        super().__init__(lifetime=1,
                         moving_speed=1,
                         center_x=start_x,
                         center_y=start_y)
        temp_text = arcade.draw_text(text, start_x, start_y, arcade.color.WHITE)
        self.texture = temp_text.texture
        self.move_to(start_x, start_y + 10, rotate=False, set_target=False)
