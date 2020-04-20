"""
map.py
Manages everything related to how walls, backgrounds, levels and the entire dungeon is generated.
Pathfinding will also depend on objects here, and is thus integral to it's functionality.
"""

from __future__ import annotations

import json

import arcade
import numpy as np

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

    def render(self) -> None:
        """
        Calls render on all level
        """

        for column in self.levels:
            for level in column:
                if level is not None:
                    print('Rendering Level')
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
        # self.entrances = []

    @staticmethod
    def load_file(level_x: int, level_y: int, path: str) -> Level:
        """
        Builds a Level from a given file path.

        :param path: Path to the Level file.
        :return: The new generated Level file.
        """

        level = Level(level_x, level_y)
        with open(path) as file:
            data = json.load(file)
            # Loads elements and structure data from level file
            level.sprites = data['elements']
            level.structure = data['structure']

        level_scale = 10 * Config.TILE_SCALING * Config.TILE_WIDTH
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
        level.floorSprites.move(level_scale * level_x, level_scale * level_y)
        level.wallSprites.move(level_scale * level_x, level_scale * level_y)

        return level

    def render(self) -> None:
        """
        Calls render on all sprites.
        """
        x = 0
        y = 0
        level_size = 10 * Config.TILE_SCALING * Config.TILE_WIDTH

        # Create the level
        # This shows using a loop to place multiple sprites horizontally and vertically
        for y_pos in range(0, level_size, 63 * Config.TILE_SCALING):
            for x_pos in range(0, level_size, 63 * Config.TILE_SCALING):
                cur_tile = self.level[y][x]
                sprite = self.sprites[cur_tile]
                floor = arcade.Sprite(sprite, Config.TILE_SCALING)
                floor.center_x = x_pos
                floor.center_y = y_pos
                if cur_tile == ' ':
                    self.floor_list.append(floor)
                elif cur_tile == 'w':
                    self.wall_list.append(floor)
                x += 1
            x = 0
            y += 1

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
