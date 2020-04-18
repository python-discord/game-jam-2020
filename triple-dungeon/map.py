"""
map.py
Manages everything related to how walls, backgrounds, levels and the entire dungeon is generated.
Pathfinding will also depend on objects here, and is thus integral to it's functionality.
"""

from __future__ import annotations


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

        self.level_count, self.size = level_count, size
        self.levels = [[None for y in range(size)] for x in range(size)]  # array[x][y] style access


class Level(object):
    """
    A 10x10 space holding wall and background sprites, enemies, items and so forth.
    Should be loaded from

    """

    def __init__(self,) -> None:
        self.wallGrid = []

    @staticmethod
    def load_file(path: str) -> Level:
        """
        Builds a Level from a given file path.

        :param path: Path to the Level file.
        :return: The new generated Level file.
        """
        pass
