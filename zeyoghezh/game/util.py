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
        except KeyboardInterrupt:
            raise
        except BaseException:
            logging.error("Got error!", exc_info=True)
            raise

    return inner


def closest_distance_between_planets(planet1, planet2):
    # Only works cuz the planets are circles
    center_distance = arcade.get_distance_between_sprites(planet1, planet2)
    planet1_radius = planet1.height / 2
    planet2_radius = planet2.height / 2
    closest_distance = center_distance - planet1_radius - planet2_radius
    logger.debug(f"{center_distance=}, {closest_distance=}")
    return closest_distance
