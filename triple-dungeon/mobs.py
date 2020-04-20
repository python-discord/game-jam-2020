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
        self.character_dir = Enums.FRONT_FACING  # Face front by default.

        # for i in range(4):
        #     texture = arcade.load_texture(f"{main_path}knight iso char_idle_{i}.png")
        #     self.idle_textures.append(texture)
        #
        # # Load textures for running horizontally
        # for i in range(6):
        #     self.walking_textures.append([arcade.load_texture(f"{main_path}knight iso char_run left_{i}.png"),
        #                                   arcade.load_texture(f"{main_path}knight iso char_run left_{i}.png",
        #                                                       mirrored=True)])
        #
        # # Load textures for running down
        # for i in range(5):
        #     self.down_textures.append(arcade.load_texture(f"{main_path}knight iso char_run down_{i}.png"))
        #
        # # Load textures for running up
        # for i in range(5):
        #     self.up_textures.append(arcade.load_texture(f"{main_path}knight iso char_run up_{i}.png"))

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """
        Updates animations for the Player.
        :param delta_time: No idea.
        """

        # Figure out if we need to flip face left, right, up, or down
        # if self.change_x > 0:
        #     self.character_dir = Enums.LEFT_FACING
        # elif self.change_x < 0:
        #     self.character_dir = Enums.RIGHT_FACING
        # elif self.change_x == 0 and self.change_y == 0:
        #     self.character_dir = Enums.FRONT_FACING

        if self.change_x == 0 and self.change_y == 0:
            self.texture = next(self.animations.idles)
        elif self.change_y > 0:  # Up
            self.texture = next(self.animations.up)
        elif self.change_y < 0:  # Down
            self.texture = next(self.animations.down)
        elif self.change_x > 0:  # Left
            self.texture = next(self.animations.right)
        elif self.change_x < 0:  # Right
            self.texture = next(self.animations.left)

        # Idle Animation
        # if self.change_x == 0 and self.change_y == 0:
        #     self.cur_texture = (self.cur_texture + 1) % (Config.RUN_UPDATES_PER_FRAME * 3)
        #     self.texture = self.idle_textures[self.cur_texture // Config.IDLE_UPDATES_PER_FRAME]
        #     return
        #
        # # walk up animation
        # if self.change_y > 0:
        #     self.cur_texture = (self.cur_texture + 1) % (Config.RUN_UPDATES_PER_FRAME * 4)
        #     self.texture = self.up_textures[self.cur_texture // Config.RUN_UPDATES_PER_FRAME]
        #     return
        #
        # # walk down animation
        # if self.change_y < 0:
        #     self.cur_texture = (self.cur_texture + 1) % (Config.RUN_UPDATES_PER_FRAME * 4)
        #     self.texture = self.down_textures[self.cur_texture // Config.RUN_UPDATES_PER_FRAME]
        #     return

        # # Walking left/right animation
        # self.cur_texture = (self.cur_texture + 1) % (Config.RUN_UPDATES_PER_FRAME * 5)
        # self.texture = self.walking_textures[self.cur_texture // Config.RUN_UPDATES_PER_FRAME][self.character_dir.value]

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
