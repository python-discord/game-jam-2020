import math
from typing import Tuple

import arcade

from triple_vision import Tile


def load_texture_pair(filename: str) -> Tuple[arcade.Texture, arcade.Texture]:
    return (
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    )


def is_in_radius(center_object: arcade.Sprite, target_object: arcade.Sprite, radius: int) -> bool:
    return is_in_radius_positions(center_object.position, target_object.position, radius)


def is_in_radius_positions(
        center_position: Tuple[float, float],
        target_position: Tuple[float, float],
        radius: int
        ):
    return (
            abs(center_position[0] - target_position[0]) <= radius and
            abs(center_position[1] - target_position[1]) <= radius
    )


def tile_to_pixels(x: int, y: int) -> Tuple[float, float]:
    return (
        x * Tile.SCALED + Tile.SCALED / 2,
        y * Tile.SCALED + Tile.SCALED / 2
    )


def pixels_to_tile(x: float, y: float) -> Tuple[int, int]:
    return (
        int((x - (x % Tile.SCALED)) / Tile.SCALED),
        int((y - (y % Tile.SCALED)) / Tile.SCALED)
    )

def distance_between(center_object: arcade.Sprite, target_object: arcade.Sprite) -> float:
    x_diff = target_object.center_x - center_object.center_x
    y_diff = target_object.center_y - center_object.center_y
    return math.hypot(x_diff, y_diff)


def get_change_vector(
        *,
        start_position: Tuple[float, float],
        destination_position: Tuple[float, float],
        speed_multiplier: float = 1.0
) -> Tuple[float, float, float]:
    """
    Get x, y change resulting in a angle that will go from start object center to end object
    center. To reverse direction reverse the object arguments.
    :param start_position: starting position
    :param destination_position: ending position
    :param speed_multiplier: change x,y will be multiplied by this amount
    :return: Tuple[change_x, change_y, angle]
    """
    dest_x = destination_position[0]
    dest_y = destination_position[1]

    start_x = start_position[0]
    start_y = start_position[1]

    x_diff = dest_x - start_x
    y_diff = dest_y - start_y
    angle = math.atan2(y_diff, x_diff)

    change_x = math.cos(angle) * speed_multiplier
    change_y = math.sin(angle) * speed_multiplier

    return change_x, change_y, angle
