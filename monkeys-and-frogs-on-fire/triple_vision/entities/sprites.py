import math
import time

import arcade

from triple_vision.constants import SCALED_TILE


class MovingSprite(arcade.Sprite):
    def __init__(self, moving_speed, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed = moving_speed
        self.target = None

    def move_to(self, x, y, rotate: bool = True) -> None:
        """
        Move the MovingSprite into a given point on the screen.

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

        self.target = (x, y)

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


class Bullet(MovingSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # keep the time of the bullet creation
        self.shot_at = time.time()
