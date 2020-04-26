
import Textures

from Enemy import Enemy

class SpikyBall(Enemy):
    def __init__(self, x, y):
        super().__init__(Textures.get_texture(1, 1), x, y)

        self.movespeed = 2.5
        self.damage = 2
    
    def update(self):

        if self.intersects(self.level.player):
            self.removed = True

        super().update()

    def move_to(self, entity):
        if self.center_x > entity.center_x:
            self.change_x = -self.movespeed
        elif self.center_x < entity.center_x:
            self.change_x = self.movespeed
        