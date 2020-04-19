from enum import IntEnum


TITLE = 'Triple Vision'
WINDOW_SIZE = (1280, 720)

SCALING = 3
TILE_SIZE = 16
SCALED_TILE = TILE_SIZE * SCALING


SOUND_FADE_FREQUENCY = 0.1
SOUND_FADE_AMOUNT = 0.05


class Direction(IntEnum):
    LEFT: int = 1
    RIGHT: int = 0
