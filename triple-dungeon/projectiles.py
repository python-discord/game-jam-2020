"""
projectiles.py
Organizes classes related to projectiles
"""

import arcade


class Projectile(arcade.Sprite):
    """
    Represents a Projectile. Damage, sprite, speed, range, collision list?
    """
    def __init__(self, speed=7, damage=0, range=100, *args, **kwargs) -> None:
        # Set up parent class
        super().__init__()

        self.speed = speed
        self.damage = damage  # unimplemented
        self.texture = None
        self.range = range  # unimplemented
        self.collision_list = []


class Temp(Projectile):
    """
    Temporary extension of projectile to demonstrate usage
    """
    def __init__(self, *args, **kwargs) -> None:
        super(Temp, self).__init__(*args, **kwargs)
        self.texture = arcade.load_texture("resources/images/monsters/frog/frog1.png")
        self.speed = 12
        self.scale = 4
        # collision list for who/what to collide with: wall, player, enemy

    # Can place function for starting on player or enemy
