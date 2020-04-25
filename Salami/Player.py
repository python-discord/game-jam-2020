

import LevelGenerator
import Textures

from Constants import TILE_SIZE, ROOM_WIDTH, ROOM_HEIGHT
from Mob import Mob

class Player(Mob):

    def __init__(self, texture, x, y, keyboard):
        super().__init__(texture, x, y)

        self.keyboard = keyboard

        self.movespeed = 2.5
        self.jump_height = 4
        self.jumping = False

        self.curr_jump_height = 0
        self.min_jump_height = 8
        self.max_jump_height = 64

        self.walk_count = 0
        self.walk_frame_speed = 8
        self.player_dir = True

        self.curr_dash_frame = 0
        self.max_dash_frame = 12
        self.dashing = False

        self.idle_texture = Textures.get_texture(0, 4)
        self.idle_texture_mirrored = Textures.get_texture(0, 5)
        self.walking_textures = Textures.get_textures(1, 4, 4)
        self.walking_textures_mirrored = Textures.get_textures(1, 5, 4)
        self.dash_textures = Textures.get_textures(5, 4, 3)
        self.dash_textures_mirrored = Textures.get_textures(5, 5, 3)
        self.crawl_textures = Textures.get_textures(8, 4, 3)
        self.crawl_textures_mirrored = Textures.get_textures(8, 5, 3)
    
    def update(self):

        speed_mult = 1
        if self.keyboard.is_pressed("sprint"):
            speed_mult = 2
        
        if self.keyboard.is_pressed("dash"):
            self.dashing = True
            # level_gen_x = self.center_x // TILE_SIZE // ROOM_WIDTH
            # level_gen_y = self.center_y // TILE_SIZE // ROOM_HEIGHT

            # LevelGenerator.generateLevel(self.level, int(level_gen_x), int(level_gen_y))

        if self.keyboard.is_pressed("attack"):
            self.level.ball.center_x = self.center_x
            self.level.ball.center_y = self.center_y
            self.level.ball.change_x = self.change_x * 1.5
            self.level.ball.change_y = self.change_y * 2

        if self.keyboard.is_pressed("jump"):
            if self.level.physics_engine.can_jump(1):
                self.level.physics_engine.jump(self.jump_height)
                self.jumping = True
            elif self.level.physics_engine.can_jump(-1):
                self.jumping = False
                self.curr_jump_height = 0
                
            if self.curr_jump_height > self.max_jump_height:
                self.jumping = False
                self.curr_jump_height = 0

        elif (self.curr_jump_height >= self.min_jump_height):
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
            elif self.change_x < -1:
                self.change_x += 1
            else:
                self.change_x = 0

        if self.dashing:
            if self.change_x > 0:
                self.change_x = self.movespeed * speed_mult * 2
            elif self.change_x < 0:
                self.change_x = -self.movespeed * speed_mult * 2

            self.curr_dash_frame += 1
            if self.curr_dash_frame >= self.max_dash_frame * len(self.dash_textures):
                self.curr_dash_frame = 0
                self.dashing = False

        self.walk_count += 1
        if self.walk_count >= len(self.walking_textures) * self.walk_frame_speed:     
            self.walk_count = 0
        
        if self.change_x > 0:
            if self.dashing:
                self.texture = self.dash_textures[self.curr_dash_frame // self.max_dash_frame]
            else:
                self.texture = self.walking_textures[self.walk_count // self.walk_frame_speed]
            self.player_dir = True

        elif self.change_x < 0:
            if self.dashing:
                self.texture = self.dash_textures_mirrored[self.curr_dash_frame // self.max_dash_frame]
            else:
                self.texture = self.walking_textures_mirrored[self.walk_count // self.walk_frame_speed]
            self.player_dir = False
        else:
            if self.player_dir:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture_mirrored

        super().update()