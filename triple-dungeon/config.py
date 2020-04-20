"""
config.py
Holds all constants used for setting up the game.
May later hold functions for loading/saving configuration files.
"""


class Config(object):
    """
    A simple class dedicated to loading, storing and organizing constants.
    """

    # Constants
    SCREEN_WIDTH = 1650
    SCREEN_HEIGHT = 1000
    SCREEN_TITLE = "Triple Dungeon"
    TILE_WIDTH = 63
    UPDATES_PER_FRAME = 20

    # Constants used to scale our sprites from their original size
    CHARACTER_SCALING = 1
    TILE_SCALING = 2

    # Movement speed of player, in pixels per frame
    PLAYER_MOVEMENT_SPEED = 7

    # How many pixels to keep as a minimum margin between the character
    # and the edge of the screen.
    LEFT_VIEWPORT_MARGIN = 250
    RIGHT_VIEWPORT_MARGIN = 250
    BOTTOM_VIEWPORT_MARGIN = 50
    TOP_VIEWPORT_MARGIN = 100
