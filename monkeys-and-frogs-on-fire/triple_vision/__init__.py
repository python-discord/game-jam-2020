from enum import IntEnum


class Settings:
    TITLE = 'Triple Vision'
    WINDOW_SIZE = (1280, 720)
    SCALING = 3


class Tile:
    SIZE = 16
    SCALED = SIZE * Settings.SCALING


class SoundSettings:
    FADE_FREQUENCY = 0.1
    FADE_AMOUNT = 0.05


class Direction(IntEnum):
    LEFT: int = 1
    RIGHT: int = 0
