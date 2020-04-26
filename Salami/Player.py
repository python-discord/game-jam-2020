
import arcade
import math

import LevelGenerator
import Textures

from Constants import TILE_SIZE, ROOM_WIDTH, ROOM_HEIGHT
from Mob import Mob
from Projectile import Projectile

class Player(Mob):

    def __init__(self, x, y, keyboard):

        self.keyboard = keyboard

        self.movespeed = 2.5
        self.jump_height = 4
        self.jumping = False

        self.max_attack_speed = 12
        self.curr_attack_speed = 0
        self.attack_dir = 0

        self.curr_jump_height = 0
        self.min_jump_height = 8
        self.max_jump_height = 64

        self.walk_count = 0
        self.walk_frame_speed = 8

        self.not_mirrored = True

        self.curr_dash_frame = 0
        self.dash_frame_speed = 12
        self.dashing = False

        self.crawling = False
        self.curr_crawl_frame = 0
        self.crawl_frame_speed = 16

        self.health = 9
        self.curr_invis_frame = 0
        self.invis_frame = 90

        # Textures
        self.idle_texture = Textures.get_texture(0, 4)
        self.idle_texture_mirrored = Textures.get_texture(0, 5)
        self.walking_textures = Textures.get_textures(1, 4, 4)
        self.walking_textures_mirrored = Textures.get_textures(1, 5, 4)
        self.dash_textures = Textures.get_textures(5, 4, 3)
        self.dash_textures_mirrored = Textures.get_textures(5, 5, 3)
        self.crawl_textures = Textures.get_textures(7, 4, 4)
        self.crawl_textures_mirrored = Textures.get_textures(7, 5, 4)

        super().__init__(self.idle_texture, x, y)
    
    def update(self):

        speed_mult = 1
        if self.keyboard.is_pressed("sprint"):
            speed_mult = 2
        
        if self.keyboard.is_pressed("dash"):
            if not self.dashing:
                self.change_y += 2
                if self.health > 0:
                    self.health -= 1 
            self.dashing = True
        
        if self.keyboard.is_pressed("l"):
            self.level.reset = True

        if self.keyboard.is_pressed("down"):
            # if not self.crawling:
            self.change_y -= 0.1
            self.crawling = True
            speed_mult *= 0.5
        else:
            self.crawling = False

        if self.keyboard.is_pressed("attack"):
            if self.curr_attack_speed == 0:

                extra_y_dir = 0
                if self.keyboard.is_pressed("up"):
                    extra_y_dir = 4
                elif self.keyboard.is_pressed("down"):
                    extra_y_dir = -4

                attack_x = (self.change_x) * 4
                attack_y = (self.change_y + extra_y_dir) * 3
                attack_angle = int(math.atan2(attack_y, attack_x)/math.pi*180)

                card = Projectile(
                    Textures.SPRITESHEET[3 + int((attack_angle % 360) / 45) + 16],
                    self.center_x,
                    self.center_y,
                    attack_x,
                    attack_y)
                self.level.add_entity_to_list(card, self.level.entities)
                self.curr_attack_speed = self.max_attack_speed

        if self.curr_attack_speed > 0:
            self.curr_attack_speed -= 1

        if self.keyboard.is_pressed("jump"):
            if self.level.physics_engine.can_jump(1):
            # if self.level.engine.can_jump(self, 1):
                self.level.physics_engine.jump(self.jump_height)
                self.jumping = True
            # elif self.level.engine.can_jump(self, -1):
            elif self.level.physics_engine.can_jump(-1):
                self.jumping = False
                self.curr_jump_height = 0
                
            if self.curr_jump_height > self.max_jump_height:
                self.jumping = False
                self.curr_jump_height = 0

        elif self.curr_jump_height >= self.min_jump_height:
            self.jumping = False
            self.curr_jump_height = 0
        
        if self.jumping:
            self.change_y = self.jump_height
            self.curr_jump_height += self.jump_height

        if self.keyboard.is_pressed("left"):
            self.change_x = -self.movespeed * speed_mult
        elif self.keyboard.is_pressed("right"):
            self.change_x = self.movespeed * speed_mult
        else:
            if self.change_x > 1:
                self.change_x -= 1
                self.not_mirrored = True
            elif self.change_x < -1:
                self.change_x += 1
                self.not_mirrored = False
            else:
                self.change_x = 0

        if self.dashing:
            if self.change_x > 0:
                self.change_x = self.movespeed * speed_mult * 2
            elif self.change_x < 0:
                self.change_x = -self.movespeed * speed_mult * 2

            self.curr_dash_frame += 1
            if self.curr_dash_frame >= self.dash_frame_speed * len(self.dash_textures):
                self.curr_dash_frame = 0
                self.dashing = False

        elif self.crawling:
            self.curr_crawl_frame += 1
            if self.curr_crawl_frame >= self.crawl_frame_speed * len(self.crawl_textures):
                self.curr_crawl_frame = 0
        else:
            self.walk_count += 1
            if self.walk_count >= len(self.walking_textures) * self.walk_frame_speed:     
                self.walk_count = 0
        
        if self.curr_invis_frame > 0 and self.curr_invis_frame % 12 < 6:
            self.texture = Textures.get_texture(15, 15)
        elif self.change_x > 0:
            if self.dashing:
                self.texture = self.dash_textures[self.curr_dash_frame // self.dash_frame_speed]
            elif self.crawling:
                self.texture = self.crawl_textures[self.curr_crawl_frame // self.crawl_frame_speed]
            else:
                self.texture = self.walking_textures[self.walk_count // self.walk_frame_speed]
            # self.player_dir = True

        elif self.change_x < 0:
            if self.dashing:
                self.texture = self.dash_textures_mirrored[self.curr_dash_frame // self.dash_frame_speed]
            elif self.crawling:
                self.texture = self.crawl_textures_mirrored[self.curr_crawl_frame // self.crawl_frame_speed]
            else:
                self.texture = self.walking_textures_mirrored[self.walk_count // self.walk_frame_speed]
            # self.player_dir = False
        else:
            if self.not_mirrored:
                if self.crawling:
                    self.texture = self.crawl_textures[0]
                else:
                    self.texture = self.idle_texture
            else:
                if self.crawling:
                    self.texture = self.crawl_textures_mirrored[0]
                else:
                    self.texture = self.idle_texture_mirrored

        super().update()

    def collided(self, entity, dx, dy):
        super().collided(entity, dx, dy)

    def hurt(self, damage, knockback):
        if damage == 0:
            return
        if self.curr_invis_frame <= 0:
            self.health -= damage
            self.change_x += knockback
            self.curr_invis_frame = self.invis_frame

        if self.health <= 0:
            # Die
            pass