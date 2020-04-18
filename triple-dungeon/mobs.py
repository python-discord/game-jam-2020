import arcade

from config import Config

class Mob(object):
    """
    Represents a Mob. No defined behaviour, it has no intelligence.
    """
    def __init__(self, sprite, max_health=100, max_armor=0) -> None:
        self.sprite_path = sprite
        self.sprite = arcade.Sprite(self.sprite_path, Config.CHARACTER_SCALING)
        self.max_health, self.max_armor = max_health, max_armor
        self.health, self.armor = max_health, max_armor

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
