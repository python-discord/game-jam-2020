"""
mobs.py
Organizes all classes related to Mobs, Entities, Enemies, Players and Items.
"""

import arcade

from config import Config

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

        main_path = "resources/images/character/knight/"

        # Load textures for idle standing
        for i in range(4):
            texture = arcade.load_texture(f"{main_path}knight iso char_idle_{i}.png")
            self.idle_textures.append(texture)
        
    def update_animation(self, delta_time: float = 1/60):
        # idle animation
        self.cur_texture += 1
        if self.cur_texture > 3 * Config.UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.idle_textures[self.cur_texture // Config.UPDATES_PER_FRAME]
        print('test')

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

    def get_enemy(self):
        return self

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
