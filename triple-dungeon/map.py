"""
map.py
Manages everything related to how walls, backgrounds, levels and the entire dungeon is generated.
Pathfinding will also depend on objects here, and is thus integral to it's functionality.
"""

from __future__ import annotations
from config import Config

import arcade
import json
import numpy as np

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
        # setup
        self.floor_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        level_size =  10 * Config.TILE_SCALING * Config.TILE_WIDTH

        # get center level

        center = Level()
        center.load_file('resources/levels/map1/center.json')
        center.render()
        center_floor, center_wall = center.get_lists()
        self.floor_list.extend(center_floor)
        self.wall_list.extend(center_wall)


        # get a side room
        room = Level()
        room.load_file('resources/levels/map1/room.json')
        room.rotate_level(2)
        room.render()
        room_floor, room_wall = room.get_lists()
        room_floor.move(level_size, 0)
        room_wall.move(level_size, 0)
        self.floor_list.extend(room_floor)
        self.wall_list.extend(room_wall)

        # get a side room
        room = Level()
        room.load_file('resources/levels/map1/room.json')
        room.render()
        room_floor, room_wall = room.get_lists()
        room_floor.move(-level_size, 0)
        room_wall.move(-level_size, 0)
        self.floor_list.extend(room_floor)
        self.wall_list.extend(room_wall)


        #self.level_count, self.size = level_count, size
        #self.levels = [[None for y in range(size)] for x in range(size)]  # array[x][y] style access

    def add_level(self, sprit_list):
        for x in sprit_list:
            self.levels.append(x)

    def render(self) -> None:
        """
        Calls render on all level
        """

        for column in self.levels:
            for level in column:
                if level is not None:
                    level.render()


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
        self.level = []

        # Tuples containing the Node positions of where walls, floor and entrances are.
        # All positions are generated based on the level's X and Y position, so that all points within
        # the dungeon can be mapped by a proper pathfinding system.
        self.floor_list = []
        self.wall_list = []
        #self.entrances = []

    #@staticmethod
    def load_file(self, path: str) -> Level:
        """
        Builds a Level from a given file path.

        :param path: Path to the Level file.
        :return: The new generated Level file.
        """
        self.floor_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        

        with open(path) as file:
            level = json.load(file)
        self.sprites = level['elements']
        self.level = level['structure']
        
    def render(self) -> None:
        """
        Calls render on all sprites.
        """
        x = 0
        y = 0
        level_size = 10 * Config.TILE_SCALING * Config.TILE_WIDTH

        # Create the level
        # This shows using a loop to place multiple sprites horizontally and vertically
        for y_pos in range(0, level_size , 63 * Config.TILE_SCALING):
            for x_pos in range(0, level_size, 63 * Config.TILE_SCALING):
                cur_tile = self.level[y][x]
                sprite = self.sprites[cur_tile]
                floor = arcade.Sprite(sprite, Config.TILE_SCALING)
                floor.center_x = x_pos
                floor.center_y = y_pos
                if(cur_tile == ' '):
                    self.floor_list.append(floor)
                elif(cur_tile == 'w'):
                    self.wall_list.append(floor)
                x += 1
            x = 0
            y += 1

    def get_lists(self):
        return (self.floor_list, self.wall_list)

    def rotate_level(self, times_rotated):
        m = np.array(self.level)
        for i in range(0, times_rotated):
            m = np.rot90(m)
        self.level = m.tolist()