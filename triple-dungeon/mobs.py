import arcade

class Mob(object):
    def __init__(self, sprite, max_health=100, max_armor=0) -> None:
        self.sprite_path = sprite
        self.max_health, self.max_armor = max_health, max_armor
        self.health, self.armor = max_health, max_armor

    def tick(self) -> None:
        pass

class Player(Mob):
    def __init__(self, *args, **kwargs) -> None:
        super(Player, self).__init__(*args, **kwargs)

class Enemy(Mob):
    def __init__(self, *args, **kwargs) -> None:
        super(Enemy, self).__init__(*args, **kwargs)

    def tick(self) -> None:

    def path(self) -> None:
