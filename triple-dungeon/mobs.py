"""
mobs.py
Organizes all classes related to Mobs, Entities, Enemies, Players and Items.
"""

import arcade

from config import Config, Enums, SpritePaths
from sprites import PlayerAnimations


class Mob(arcade.Sprite):
    """
    Represents a Mob. No defined behaviour, it has no intelligence.
    """

    def __init__(self, max_health=100, max_armor=0, *args, **kwargs) -> None:
        # Set up parent class
        super().__init__()

        self.max_health, self.max_armor = max_health, max_armor
        self.health, self.armor = max_health, max_armor
        self.idle_textures = []
        self.walking_textures = []
        self.up_textures = []
        self.down_textures = []
        self.cur_texture = 0


        # Used for mapping directions to animations
        self.map = {
            Enums.IDLE : self.animations.idles,
            Enums.UP : self.animations.up,
            Enums.DOWN : self.animations.down,
            Enums.RIGHT : self.animations.right,
            Enums.LEFT : self.animations.left
        }

    def tick(self) -> None:
        """
        A on_update function, the Mob should decide it's next actions here.
        """
        pass


class Player(Mob):
    """
    Represents a Player.
    While this is a instance, there should only be one in the world at any given time.
    """

    def __init__(self, *args, **kwargs) -> None:
        super(Player, self).__init__(*args, **kwargs)

        self.animations = PlayerAnimations(SpritePaths.KNIGHT)
        self.refreshIndex = 0

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """
        Updates animations for the Player.
        :param delta_time: No idea.
        """

        self.refreshIndex = (self.refreshIndex + 1) % Config.RUN_UPDATES_PER_FRAME

        if self.change_x == 0 and self.change_y == 0: # Idle
            dir = Enums.IDLE
        elif self.change_y > 0:  # Up
            dir = Enums.UP
        elif self.change_y < 0:  # Down
            dir = Enums.DOWN
        elif self.change_x > 0:  # Left
            dir = Enums.LEFT
        elif self.change_x < 0:  # Right
            dir = Enums.RIGHT

        if self.prev != dir or not wait:
            self.texture = next(self.map[dir])

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

    def tick(self) -> None:
        """
        A on_update function, the Enemy Mob should scan for the player, decide how to path to it, and
        decide how to take offensive action.
        """
        pass

    def path(self) -> None:
        """
        Not yet decided how this function should work.
        Basically, most pathfinding decisions should be kept within this function.
        """
        pass
