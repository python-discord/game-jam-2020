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
    RUN_UPDATES_PER_FRAME = 8

    # Constants used to scale our sprites from their original size
    CHARACTER_SCALING = 1
    TILE_SCALING = 2
    TILE_SIZE = TILE_WIDTH * TILE_SCALING

    # The number of pixels across the level
    LEVEL_SIZE = 10 * TILE_SCALING * TILE_WIDTH

    # Movement speed of player, in pixels per frame
    PLAYER_MOVEMENT_SPEED = 14

    # How many pixels to keep as a minimum margin between the characters and the edge of the screen.
    LEFT_VIEWPORT_MARGIN = 700
    RIGHT_VIEWPORT_MARGIN = 700
    BOTTOM_VIEWPORT_MARGIN = 300
    TOP_VIEWPORT_MARGIN = 350

    # All debug statements and renderings should use this
    DEBUG = False
    
    #Monster Count to be spawned
    MONSTER_COUNT = 0


class Enums(Enum):
    """
    A simple class used for tracking different simple
    """

    # Player Direction Enums
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    IDLE = 4


class SpritePaths(object):
    """
    Simple class for holding sprite paths.
    """

    __CHARACTERS = os.path.join(IMAGES, "characters")
    __MONSTERS = os.path.join(IMAGES, "monsters")

    # Single frame sprites
    SKELETON = os.path.join(__MONSTERS,  "skeleton.png")
    GHOST = os.path.join(__MONSTERS, "ghost", "ghost1.png")
    FROG = os.path.join(__MONSTERS, "frog", "frog1.png")

    # Animated sprites
    KNIGHT = os.path.join(__CHARACTERS, "knight")
