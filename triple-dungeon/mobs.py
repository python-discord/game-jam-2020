"""
mobs.py
Organizes all classes related to Mobs, Entities, Enemies, Players and Items.
"""

from typing import List, Tuple

import arcade
from config import Config, Enums, SpritePaths
from map import Dungeon
from sprites import PlayerAnimations


class Mob(arcade.Sprite):
    """
    Represents a Mob. No defined behaviour, it has no intelligence.
    """

    def __init__(self, dungeon: Dungeon, max_health=100, max_armor=0, *args, **kwargs) -> None:
        # Set up parent class
        super(Mob, self).__init__(*args, **kwargs)

        self.max_health, self.max_armor = max_health, max_armor
        self.health, self.armor = max_health, max_armor
        self.idle_textures = []
        self.walking_textures = []
        self.up_textures = []
        self.down_textures = []
        self.cur_texture = 0

        self.dungeon = dungeon
        self.target = None

    
class Player(Mob):
    """
    Represents a Player.
    While this is a instance, there should only be one in the world at any given time.
    """

    def __init__(self, *args, **kwargs) -> None:
        super(Player, self).__init__(*args, **kwargs)

        self.animations = PlayerAnimations(SpritePaths.KNIGHT)
        # Used for mapping directions to animations
        self.map = {
            Enums.IDLE: self.animations.idles,
            Enums.UP: self.animations.up,
            Enums.DOWN: self.animations.down,
            Enums.RIGHT: self.animations.right,
            Enums.LEFT: self.animations.left
        }

        self.refreshIndex = 0
        self.prev = Enums.IDLE
        self.texture = next(self.map[self.prev])
        self.kill_list = []
        self.cur_recipe = None

    def add_kill(self, creature):
        # Adds a kill to kill_list. If 3 or more check the recipe then give a power up if it matches.
        self.kill_list.append(creature)
        print(self.kill_list)
        print(self.cur_recipe)
        if self.cur_recipe == self.kill_list:
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            self.kill_list = []
        elif len(self.kill_list) >= 3:
            self.kill_list = []

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """
        Updates animations for the Player.
        :param delta_time: No idea.
        """

        # Increase the refresh index according
        self.refreshIndex = (self.refreshIndex + 1) % Config.RUN_UPDATES_PER_FRAME

        # Logic to determine what direction we're in.
        if self.change_x == 0 and self.change_y == 0:
            cur = Enums.IDLE
        elif self.change_y > 0:  # Up
            cur = Enums.UP
        elif self.change_y < 0:  # Down
            cur = Enums.DOWN
        elif self.change_x > 0:  # Left
            cur = Enums.RIGHT
        elif self.change_x < 0:  # Right
            cur = Enums.LEFT
        else:  # Idle
            cur = Enums.IDLE

        # If we're in a new direction or the refresh index has reset
        if self.prev is not cur or self.refreshIndex == 0:
            self.texture = next(self.map[cur])

        self.prev = cur

    def tick(self):
        """
        While Player objects do not have any AI (they are controlled by the user),
        the tick function can keep track of statistics that progress over time, like
        regenerating health/armor or status effects like poison.
        """


class Enemy(Mob):
    """
    Represents an Enemy Mob.
    Will take basic offensive actions against Player objects.
    """

    def __init__(self, *args, **kwargs) -> None:
        super(Enemy, self).__init__(*args, **kwargs)
        self.monster_type = ''

    def nearestPosition(self) -> Tuple[int, int]:
        """
        Returns the nearest absolute dungeon tile the Mob is placed on.

        :return: A tuple containing the Mob's dungeon tile position.
        """
        return (round(self.center_x / Config.TILE_SIZE),
                round(self.center_y / Config.TILE_SIZE))

    def tick(self, path: Tuple[int, int] = None) -> None:
        """
        A on_update function, the Mob should decide it's next actions here.
        """
        curpos, nextpos = self.nearestPosition(), path[1]
        # print(curpos, nextpos)

        if nextpos[0] > curpos[0]:
            self.change_x = Config.PLAYER_MOVEMENT_SPEED - 3
        elif nextpos[0] < curpos[0]:
            self.change_x = -Config.PLAYER_MOVEMENT_SPEED + 3
        else:
            self.change_x = 0

        if nextpos[1] > curpos[1]:
            self.change_y = Config.PLAYER_MOVEMENT_SPEED - 3
        elif nextpos[1] < curpos[1]:
            self.change_y = -Config.PLAYER_MOVEMENT_SPEED + 3
        else:
            self.change_y = 0

        # print(self.change_x, self.change_y)

    def get_path(self, end: Tuple[int, int] = None) -> List[Tuple[int, int]]:
        """
        Returns the path to get to the Mob's target in absolute integer positions.

        :param end: A the endpoint tuple. Must be a valid position within the matrix.
        :return:
        """
        if end is None:
            end = self.target.position
            start, end = self.nearestPosition(), (round(end[0] / Config.TILE_SIZE), round(end[1] / Config.TILE_SIZE))
            start, end = self.dungeon.grid.node(*start), self.dungeon.grid.node(*end)
            paths, runs = self.dungeon.finder.find_path(start, end, self.dungeon.grid)
            self.dungeon.grid.cleanup()
            return paths
