"""
mobs.py
Organizes all classes related to Mobs, Entities, Enemies, Players and Items.
"""

from typing import List, Tuple

import arcade
import random
import math

from config import Config, Enums, SpritePaths
from map import Dungeon
from sprites import PlayerAnimations

class MobHandler:

    def __init__(self):
        super().__init__()
        self.enemy_list = []
        self.avoid_list = []
        self.dungeon = None
        self.player = None

    def setup(self, ghost, frogs, player, dungeon) -> list:
        self.enemy_list = arcade.SpriteList()
        self.dungeon = dungeon
        self.player = player
        self.avoid_list = arcade.SpriteList()
        self.avoid_list.append(self.player)
        for d in dungeon.getWalls():
            self.avoid_list.append(d)

        for count in range(ghost):
            mob = Enemy(filename="resources/images/monsters/ghost/ghost1.png", dungeon=self.dungeon)
            level = random.choice(self.dungeon.levelList)
            mob.center_x, mob.center_y = level.random()
            mob.target = self.player
            mob.scale = 4
            mob.monster_type = 'ghost'
            mob.collisions = arcade.PhysicsEngineSimple(mob, self.avoid_list)
            mob.level = level
            self.enemy_list.append(mob)
            self.avoid_list.append(mob)
        for count in range(frogs):
            mob = Enemy(filename="resources/images/monsters/frog/frog1.png", dungeon=self.dungeon)
            level = random.choice(self.dungeon.levelList)
            mob.center_x, mob.center_y = level.random()
            mob.target = self.player
            mob.scale = 4
            mob.monster_type = 'frog'
            mob.collisions = arcade.PhysicsEngineSimple(mob, self.avoid_list)
            mob.level = level
            self.enemy_list.append(mob)
            self.avoid_list.append(mob)

        return self.enemy_list

    def render(self) -> None:
        self.player.draw()
        self.enemy_list.draw()

    def update(self) -> None:
        #update player
        self.player.collisions.update()
        self.player.update_animation()

        # Enemy activation and update
        for enemy in reversed(self.enemy_list):
            distance = self.get_distance(enemy)
            enemy.collisions.update()
            if distance < 100 :
                self.player.health -= 1
            if (distance < 300):
                enemy.speed = Config.MONSTER_MOVEMENT_SPEED
                try:
                    path = enemy.get_path(enemy.target.position)
                    enemy.tick(path)
                except Exception:
                    import traceback
                    traceback.print_exc()
            else:
                left, right, bottom, top = arcade.get_viewport()
                if (
                    enemy.bottom > bottom and
                    enemy.top < bottom + Config.SCREEN_HEIGHT and
                    enemy.right < left + Config.SCREEN_WIDTH and
                    enemy.left > left
                    ):
                        enemy.speed = 5
                        ran = random.randint(0,1000)
                        if ran > 950:
                            print(ran)
                            try:
                                path = enemy.get_path(enemy.level.random())
                                enemy.tick(path)
                            except Exception:
                                import traceback
                                traceback.print_exc()

    def get_distance(self, enemy) -> int:
        start_x = enemy.center_x
        start_y = enemy.center_y
        end_x = self.player.center_x
        end_y = self.player.center_y
        distance = math.sqrt(math.pow(start_x - end_x, 2) + math.pow(start_y - end_y, 2))
        return distance

    @staticmethod
    def draw_path(path: List[Tuple[int, int]]) -> None:
        """
        Draws a line between positions in a list of tuple, also known as the path.
        :param path: A list of tuple positions defining a path that can be traversed.
        """

        if len(path) > 2:
            path = map(lambda point: ((point[0]) * Config.TILE_SIZE, (point[1]) * Config.TILE_SIZE), path)
            path = list(path)
            #print(path)
            for pos1, pos2 in zip(path, path[1:]):
                arcade.draw_line(*pos1, *pos2, color=arcade.color.RED)


class Mob(arcade.Sprite):
    """
    Represents a Mob. No defined behaviour, it has no intelligence.
    """

    def __init__(self, dungeon: Dungeon, max_health=100, max_armor=0, *args, **kwargs) -> None:
        # Set up parent class
        super(Mob, self).__init__(*args, **kwargs)

        self.max_health, self.max_armor = max_health, max_armor
        self.health, self.armor = 60, max_armor
        self.idle_textures = []
        self.walking_textures = []
        self.up_textures = []
        self.down_textures = []
        self.cur_texture = 0
        self.collisions = None
        self.dungeon = dungeon
        self.target = None
        self.level = None

    
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
        self.cur_recipe = None
        self.speed = 14

    def heal(self):
        self.health+=Config.HEAL_AMOUNT
        if self.health > self.max_health:
            self.health = self.max_health

    def harden(self):
        self.armor+=Config.ARMOR_AMOUNT

    def hurry(self):
        self.speed+=Config.SPEED_AMOUNT

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
        near_pos = self.nearestPosition()
        
        curpos, nextpos = near_pos, path[1]
        # print(curpos, nextpos)

        if nextpos[0] > curpos[0]:
            self.change_x = self.speed
        elif nextpos[0] < curpos[0]:
            self.change_x = -self.speed
        else:
            self.change_x = 0

        if nextpos[1] > curpos[1]:
            self.change_y = self.speed
        elif nextpos[1] < curpos[1]:
            self.change_y = -self.speed
        else:
            self.change_y = 0

    def get_path(self, end: Tuple[int, int] = None) -> List[Tuple[int, int]]:
        """
        Returns the path to get to the Mob's target in absolute integer positions.

        :param end: A the endpoint tuple. Must be a valid position within the matrix.
        :return:
        """

        start, end = self.nearestPosition(), (round(end[0] / Config.TILE_SIZE), round(end[1] / Config.TILE_SIZE))
        start, end = self.dungeon.grid.node(*start), self.dungeon.grid.node(*end)
        paths, runs = self.dungeon.finder.find_path(start, end, self.dungeon.grid)
        self.dungeon.grid.cleanup()
        return paths