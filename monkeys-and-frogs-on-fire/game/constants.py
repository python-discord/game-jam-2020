from enum import IntEnum, auto


TITLE = 'Game'
WINDOW_SIZE = (1280, 720)

SCALING = 2
TILE_SIZE = 16
SCALED_TILE = TILE_SIZE * SCALING


class Direction(IntEnum):
    LEFT: int = 1
    RIGHT: int = 0
