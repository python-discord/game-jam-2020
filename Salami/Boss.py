
import arcade

import Maths

from Enemy import Enemy

class Boss(Enemy):

    def __init__(self, x, y):
        self.texture_idle = arcade.load_texture("resources/spritesheet.png", 128, 32, 32, 32)
        self.texture_active = arcade.load_texture("resources/spritesheet.png", 160, 32, 32, 32)

        super().__init__(self.texture_idle, x, y)

        self.set_hit_box(Maths.create_hit_box(self.width, self.height))
        
        self.range = 32 * 16
        self.idle = True
        self.damage = 0

    def update(self):
        if not self.idle:
            super().update()

    def move_to(self, entity):
        if self.center_x > entity.center_x:
            self.change_x = -self.movespeed
        elif self.center_x < entity.center_x:
            self.change_x = self.movespeed
        if self.center_y < entity.center_y:
            if not self.jumping:
                self.change_y = self.jump_height
            self.jumping = True