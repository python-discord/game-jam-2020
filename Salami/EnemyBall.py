
import arcade

import Textures

from Enemy import Enemy

class EnemyBall(Enemy):

    def __init__(self, x, y):
        super().__init__(Textures.get_texture(3, 8), x, y)

    def update(self):

        super().update()
        # print(f"{self.change_x} {self.change_y}")

    def move_to(self, entity):
        pass

    def collided(self, entity, dx, dy):
        if dx != 0:
            self.change_x *= -0.6
        if dy != 0:
            self.change_y *= -0.8
            self.change_x *= 0.8
