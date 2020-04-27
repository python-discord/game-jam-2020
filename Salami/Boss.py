
import arcade

import Maths
import Textures

from Enemy import Enemy
from EnemyBall import EnemyBall

class Boss(Enemy):

    def __init__(self, x, y, difficulty):
        self.texture_idle = arcade.load_texture("resources/spritesheet.png", 128, 32, 32, 32)
        self.texture_active = arcade.load_texture("resources/spritesheet.png", 160, 32, 32, 32)

        super().__init__(self.texture_active, x, y, difficulty)

        self.set_hit_box(Maths.create_hit_box(self.width, self.height))
        print(f"{self.width} {self.height}")
        
        self.range = 32 * 16
        self.idle = False
        self.damage = 2
        self.health = 16 + 6 * self.difficulty

        self.curr_attack_frame = 0
        self.max_attack_frame = 120

    def update(self):
        if not self.idle:
            if self.texture != self.texture_active:
                self.texture = self.texture_active
            super().update()
        else:
            if self.texture != self.texture_idle:
                self.texture = self.texture_idle

    def move_to(self, entity):
        if self.center_x > entity.center_x:
            self.change_x = -self.movespeed
        elif self.center_x < entity.center_x:
            self.change_x = self.movespeed
        if self.center_y < entity.center_y:
            if not self.jumping:
                self.change_y = self.jump_height
            self.jumping = True
        if self.curr_attack_frame <= 0:
            ball = EnemyBall(Textures.get_texture(12, 3), self.center_x, self.center_y, self.difficulty)
            ball.change_x = self.change_x
            ball.change_y = self.change_y * 2
            self.level.add_entity_to_list(ball, self.level.entities)
            self.curr_attack_frame = self.max_attack_frame
        else:
            self.curr_attack_frame -= 1

    def die(self):
        self.level.reset_timer = 180

        super().die()