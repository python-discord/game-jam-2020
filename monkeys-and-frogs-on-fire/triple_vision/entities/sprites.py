import math
import time
from typing import Optional

import arcade

from triple_vision.constants import SCALED_TILE


class MovingSprite(arcade.Sprite):
    def __init__(self, moving_speed, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed = moving_speed
        self.target = None

    def move_to(self, x, y, rotate: bool = True, set_target: bool = True) -> None:
        """
        Move the MovingSprite into a given point on the screen.

        :param set_target: Represents if we want to set the point as a target -
        (the sprite will stop after reaching it)
        :param x, y: are the coordinates for the sprite to move into
        :param rotate: represents if we need to rotate the sprite or not
        """

        # Do math to calculate how to get the sprite to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the sprite will travel.
        x_diff = x - self.center_x
        y_diff = y - self.center_y

        angle = math.atan2(y_diff, x_diff)

        if rotate:
            # Angle the sprite
            self.angle = math.degrees(angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the sprite travels.
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        if set_target:
            self.target = (x, y)

    def move_to_sprite(self, sprite: arcade.Sprite, rotate: bool = True, set_target: bool = True) -> None:
        # should we return target here?
        self.move_to(sprite.center_x, sprite.center_y, rotate=rotate, set_target=set_target)

    def move_to_angle(self, angle, rotate: bool = True):
        if rotate:
            # Angle the sprite
            self.angle = math.degrees(angle)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the sprite travels.
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

    def distance_to(self, sprite: arcade.Sprite) -> float:
        x_diff = sprite.center_x - self.center_x
        y_diff = sprite.center_y - self.center_y
        return math.hypot(x_diff, y_diff)

    def update(self) -> None:
        if self.target is not None:
            if (
                self.target[0] - SCALED_TILE / 2 < self.center_x < self.target[0] + SCALED_TILE / 2 and
                self.target[1] - SCALED_TILE / 2 < self.center_y < self.target[1] + SCALED_TILE / 2
            ):
                self.change_x = 0
                self.change_y = 0

                self.target = None

        super().update()


class TemporarySprite(arcade.Sprite):
    def __init__(self, lifetime: Optional[int], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.lifetime = lifetime
        self.created_at = time.time()

    def update(self):
        if self.lifetime and time.time() - self.created_at > self.lifetime:
            self.kill()
        super().update()
