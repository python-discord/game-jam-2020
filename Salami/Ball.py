
import arcade
from Mob import Mob

class Ball(Mob):

    def update(self):
        
        # collision_list = arcade.check_for_collision_with_list(self, self.level.entities)

        # for entity in collision_list:
        #     if entity == self:
        #         continue

        #     if self.change_x != 0:
        #         self.change_x += entity.change_x
        #         self.change_x *= -0.9
        #     if self.change_y != 0:
        #         self.change_y += entity.change_y
        #         self.change_y *= -0.9

        if self.change_x > 12:
            self.change_x = 12
        elif self.change_x < -12:
            self.change_x = -12
        if self.change_y > 12:
            self.change_y = 12
        elif self.change_y < -12:
            self.change_y = -12

        super().update()
        # print(f"{self.change_x} {self.change_y}")

    def collided(self, entity, dx, dy):
        if dx != 0:
            self.change_x *= -0.6
        if dy != 0:
            self.change_y *= -0.8
            self.change_x *= 0.8
