
import arcade

import Textures

from Enemy import Enemy

class EnemyBall(Enemy):

    def __init__(self, texture, x, y, difficulty):
        super().__init__(texture, x, y, difficulty)

        self.life = 300
        self.health = 2

    def update(self):

        super().update()

        self.life -= 0
        if abs(self.change_x) < 0.1 and abs(self.change_y) <= 0.1 or self.life <= 0:
            self.removed = True
        # print(f"{self.change_x} {self.change_y}")

    def move_to(self, entity):
        pass

    def collided(self, entity, dx, dy):
        if dx != 0:
            self.change_x *= -0.6
        if dy != 0:
            self.change_y *= -0.8
            self.change_x *= 0.8

    def hurt(self, damage, knockback):
        super().hurt(damage, 0)