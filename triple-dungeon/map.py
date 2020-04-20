"""
map.py
Manages everything related to how walls, backgrounds, levels and the entire dungeon is generated.
Pathfinding will also depend on objects here, and is thus integral to it's functionality.
"""

from __future__ import annotations

import json

import arcade
import numpy as np

from itertools import chain

from config import Config


class Dungeon(object):
    """
    Organizes Level objects into an easy to render and path through object.
    """

    def __init__(self, level_count: int = 3, size: int = 3) -> None:
        """
        Initializes the Dungeon object.

        :param level_count: The number of Active Levels that should be stored within the Dungeon.
        :param size: The diameter of the dungeon. Allows for a total of size^2 slots for levels.
        """

        self.level_count = level_count
        self.size = size

        self.floor_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        center = Level.load_file(1, 1, 'resources/levels/map1/center.json')
        side = Level.load_file(2, 1, 'resources/levels/map1/room.json')

        self.levels = [
            [None, None, None],
            [center, side, None],
            [None, None, None]
        ]

    def getWalls(self):
        walls = arcade.SpriteList()
        walls.extend(
            list(chain.from_iterable(
                chain.from_iterable([level.wallSprites for level in column if level is not None]) for column in
                self.levels
            ))
        )
        return walls

    def render(self) -> None:
        """
        Calls render on all level
        """

        for column in self.levels:
            for level in column:
                if level is not None:
                    level.floorSprites.draw()
                    level.wallSprites.draw()


class Level:
    """
    A 10x10 space holding wall and background sprites, enemies, items and so forth.
    Should be loaded from

    """

    def __init__(self, level_x: int = 0, level_y: int = 0) -> None:
        """
        Initializes the level class. Defaults with no sprites, and no background.

        :param level_x: The level's X position within the Dungeon level matrix.
        :param level_y: The level's Y position within the Dungeon level matrix.
        """

        self.x, self.y = level_x, level_y
        self.sprites = []
        self.structure = []

        self.floorSprites = arcade.SpriteList()
        self.wallSprites = arcade.SpriteList()

        # Tuples containing the Node positions of where walls, floor and entrances are.
        # All positions are generated based on the level's X and Y position, so that all points within
        # the dungeon can be mapped by a proper pathfinding system.
        self.floor_list = []
        self.wall_list = []

    @staticmethod
    def load_file(level_x: int, level_y: int, path: str) -> Level:
        """
        Builds a Level from a given file path.

        :param level_x: The level's X position within the Dungeon level matrix.
        :param level_y: The level's Y position within the Dungeon level matrix.
        :param path: Path to the Level file.
        :return: The new generated Level file.
        """

        level = Level(level_x, level_y)
        with open(path) as file:
            data = json.load(file)
            # Loads elements and structure data from level file
            level.sprites = data['elements']
            level.structure = data['structure']

        tile_scale = Config.TILE_WIDTH * Config.TILE_SCALING

        # Places all of the tiles & sprites
        for x in range(0, 10):
            for y in range(0, 10):
                tilePath = level.sprites[level.structure[x][y]]
                sprite = arcade.Sprite(tilePath, Config.TILE_SCALING)
                sprite.center_x, sprite.center_y = x * tile_scale, y * tile_scale

                if 'floor' in tilePath:
                    level.floorSprites.append(sprite)
                elif 'wall' in tilePath:
                    level.wallSprites.append(sprite)
                else:
                    print(f'Could not handle Tile: {tilePath}')

        # Move everything into correct positions
        level.floorSprites.move(*level.center())
        level.wallSprites.move(*level.center())

        return level

    def center(self) -> tuple:
        """
        Returns the pixel center of the level.
        :return: A tuple containing the X and Y coordinates of the level's center
        """
        return self.x * Config.LEVEL_SIZE, self.y * Config.LEVEL_SIZE

    def rotate_level(self, times_rotated):
        """
        Rotates the
        :param times_rotated:
        :return:
        """
        m = np.array(self.level)
        for i in range(0, times_rotated % 4):
            m = np.rot90(m)
        self.level = m.tolist()
