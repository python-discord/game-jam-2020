from enum import IntEnum


TITLE = 'Triple Vision'
WINDOW_SIZE = (1280, 720)

SCALING = 3
TILE_SIZE = 16
SCALED_TILE = TILE_SIZE * SCALING

ON_CARD_HOVER_SLOWDOWN_MULTIPLIER = 50


class Direction(IntEnum):
    LEFT: int = 1
    RIGHT: int = 0
