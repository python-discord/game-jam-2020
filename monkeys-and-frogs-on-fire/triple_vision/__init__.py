from enum import IntEnum


class Settings:
    TITLE = 'Triple Vision'
    WINDOW_SIZE = (1280, 720)
    SCALING = 3
    MAP_SIZE = (50, 50)
    ON_CARD_HOVER_SLOWDOWN_MULTIPLIER = 50
    PLAYER_CENTER_Y_COMPENSATION = 6 * SCALING


class Tile:
    SIZE = 16
    SCALED = SIZE * Settings.SCALING


class SoundSettings:
    FADE_FREQUENCY = 0.1
    FADE_AMOUNT = 0.05
    DEFAULT_VOLUME = 0.25
    SOUNDTRACK_LIST = ["Monplaisir_-_06_-_Level_3.mp3", "Komiku_-_07_-_Battle_of_Pogs.mp3"]


class Direction(IntEnum):
    LEFT: int = 1
    RIGHT: int = 0
