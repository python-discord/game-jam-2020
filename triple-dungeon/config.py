"""
config.py
Holds all constants used for setting up the game.
May later hold functions for loading/saving configuration files.
"""

import os

from enum import Enum

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(BASE_PATH, "resources")
IMAGES = os.path.join(RESOURCES, "images")


class Config(object):
    """
    A simple class dedicated to loading, storing and organizing constants.
    """

    # Constants
    SCREEN_WIDTH = 1650
    SCREEN_HEIGHT = 1000
    SCREEN_TITLE = "Triple Dungeon"
    TILE_WIDTH = 63
    IDLE_UPDATES_PER_FRAME = 20
    RUN_UPDATES_PER_FRAME = 10

    # Constants used to scale our sprites from their original size
    CHARACTER_SCALING = 1
    TILE_SCALING = 2

    # Movement speed of player, in pixels per frame
    PLAYER_MOVEMENT_SPEED = 7

    # How many pixels to keep as a minimum margin between the character and the edge of the screen.
    LEFT_VIEWPORT_MARGIN = 250
    RIGHT_VIEWPORT_MARGIN = 250
    BOTTOM_VIEWPORT_MARGIN = 50
    TOP_VIEWPORT_MARGIN = 100


class Enums(Enum):
    """
    A simple class used for tracking different simple
    """

    # Play Direction Enums
    RIGHT_FACING = 0
    LEFT_FACING = 1
    FRONT_FACING = 2
    UP_FACING = 3
    DOWN_FACING = 4


class SpritePaths(object):
    """
    Simple class for holding sprite paths.
    """

    __MONSTERS = os.path.join(IMAGES, "monsters")

    SKELETON = os.path.join(__MONSTERS,  "skeleton.png")
    GHOST = os.path.join(__MONSTERS, "ghost", "ghost1.png")
    FROG = os.path.join(__MONSTERS, "frog", "frog1.png")
