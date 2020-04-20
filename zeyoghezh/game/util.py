import arcade
import math
import logging

logger = logging.getLogger()


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def log_exceptions(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException:
            logging.error("Got error!", exc_info=True)
            raise

    return inner


def get_unit_push_distance(planet_coords, other_coords):
    # TODO improve this logic
    x_distance = other_coords[0] - planet_coords[0]
    y_distance = other_coords[1] - planet_coords[1]
    distance_sum = abs(x_distance) + abs(y_distance)
    x_distance_normalized = x_distance / distance_sum
    y_distance_normalized = y_distance / distance_sum

    if planet_coords[0] > other_coords[0]:
        assert x_distance_normalized < 0
    if planet_coords[0] < other_coords[0]:
        assert x_distance_normalized > 0
    if planet_coords[0] == other_coords[0]:
        assert x_distance_normalized == 0
    if planet_coords[1] > other_coords[1]:
        assert y_distance_normalized < 0
    if planet_coords[1] < other_coords[1]:
        assert y_distance_normalized > 0
    if planet_coords[1] == other_coords[1]:
        assert y_distance_normalized == 0
    if abs(x_distance) > abs(y_distance):
        assert abs(x_distance_normalized) > abs(y_distance_normalized)
    assert abs(x_distance_normalized) + abs(y_distance_normalized) == 1, (
        f"{x_distance_normalized=}, {y_distance_normalized=}, "
        f"{planet_coords=}, {other_coords=}")
    return (x_distance_normalized, y_distance_normalized)


def closest_distance_between_planets(planet1, planet2):
    # Only works cuz the planets are circles
    center_distance = arcade.get_distance_between_sprites(planet1, planet2)
    planet1_radius = planet1.height / 2
    planet2_radius = planet2.height / 2
    closest_distance = center_distance - planet1_radius - planet2_radius
    logger.debug(f"{center_distance=}, {closest_distance=}")
    return closest_distance
