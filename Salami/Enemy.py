
import arcade

import Maths
import Textures

from Mob import Mob
from Projectile import Projectile

class Enemy(Mob):

    def __init__(self, texture, x, y, difficulty):
        super().__init__(texture, x, y)

        self.difficulty = difficulty

        self.damage = 1
        self.movespeed = 1
        self.jump_height = 3
        self.jumping = False
        self.curr_jump_cd = 0
        self.jump_cd = 30

        self.tex = texture

        # The enemy range in Manhattan distance
        self.range = 16 * 16

    def update(self):

        collision_list = arcade.check_for_collision_with_list(self, self.level.entities)

        for entity in collision_list:
            if isinstance(entity, Projectile):
                self.hurt(entity.damage, entity.change_x)

        player = self.level.player

        dist = Maths.manhattan_dist(self.center_x, self.center_y, player.center_x, player.center_y)
        if dist <= self.range:
            self.move_to(player)
        else:
            self.wander()
        
        if self.curr_invis_frame > 0 and self.curr_invis_frame % 12 < 6:
            self.texture = Textures.get_texture(15, 15)
        else:
            self.texture = self.tex

        if self.intersects(player):
            player.hurt(self.damage, self.change_x)
        
        super().update()

    def move_to(self, entity):
        if self.center_x > entity.center_x:
            self.change_x = -self.movespeed
        elif self.center_x < entity.center_x:
            self.change_x = self.movespeed
        if self.center_y < entity.center_y and self.curr_jump_cd == 0:
            if not self.jumping:
                self.change_y = self.jump_height
                self.curr_jump_cd = self.jump_cd
            self.jumping = True
        elif self.curr_jump_cd > 0:
            self.curr_jump_cd -= 1

    def wander(self):
        self.change_x = 0

    def collided(self, entity, dx, dy):
        if dy != 0:
            if self.change_y < 0:
                self.jumping = False

        super().collided(entity, dx, dy)
    
    def hurt(self, damage, knockback):
        import Sounds
        if self.curr_invis_frame <= 0:
            Sounds.play(Sounds.SKELETON_HIT)

        super().hurt(damage, knockback)

    def die(self):
        import random, Heart
        chance = random.randrange(0, 100)
        if chance > 90:
            heart = Heart.Heart(self.center_x, self.center_y)
            self.level.add_entity_to_list(heart, self.level.entities)
        super().die()