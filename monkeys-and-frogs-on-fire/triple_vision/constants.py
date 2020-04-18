from enum import IntEnum


TITLE = 'Triple Vision'
WINDOW_SIZE = (1280, 720)

SCALING = 3
TILE_SIZE = 16
SCALED_TILE = TILE_SIZE * SCALING


BULLET_SPEED = 5
BULLET_COOLDOWN = 0.5  # bullets per second
BULLET_LIFETIME = 0.75  # in seconds


class Direction(IntEnum):
    LEFT: int = 1
    RIGHT: int = 0
