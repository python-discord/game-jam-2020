

import LevelGenerator

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
        self.walk_frame_speed = 12
        self.player_dir = True
    
    def update(self):
        
        if self.keyboard.is_pressed("dash"):
            level_gen_x = self.center_x // TILE_SIZE // ROOM_WIDTH
            level_gen_y = self.center_y // TILE_SIZE // ROOM_HEIGHT

            LevelGenerator.generateLevel(self.level, int(level_gen_x), int(level_gen_y))

        if self.keyboard.is_pressed("attack"):
            self.level.ball.center_x = self.center_x
            self.level.ball.center_y = self.center_y
            self.level.ball.change_x = self.change_x * 8
            self.level.ball.change_y = self.change_y * 8

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

        speed_mult = 1
        if self.keyboard.is_pressed("sprint"):
            speed_mult = 3

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

        super().update()