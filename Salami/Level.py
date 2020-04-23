
import arcade
import pyglet.gl as gl
import random
import PIL

import LevelGenerator
import Maths

from Textures import Textures

from Engine import Engine
from Entity import Entity, Texs, Tex
from Projectile import Projectile
from Mob import Mob
from Ball import Ball
from Tile import Tile

from Constants import WIDTH, HEIGHT, \
    TILE_SIZE, GRAVITY, SQUARE_HIT_BOX, \
    ROOM_WIDTH, ROOM_HEIGHT

class Level:

    def __init__(self, camera, keyboard):

        self.camera = camera
        self.keyboard = keyboard

        self.tile_list = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.entities = arcade.SpriteList()
        self.tiles = {}

        self.width = WIDTH // TILE_SIZE
        self.height = HEIGHT // TILE_SIZE

        self.movespeed = 1
        self.jump_height = 4
        self.jumping = False

        self.curr_jump_height = 0
        self.min_jump_height = 8
        self.max_jump_height = 64

        # for i in range(100):
        #     ball = Ball(Texs.BALL, 128 + 128 * random.random(), 128 + 128 * random.random())
        #     ball.change_x = random.randint(-8, 8)
        #     ball.change_y = random.randint(-8, 8)
        #     self.add_entity_to_list(ball, self.entities)

        # print(f"{self.left} {self.right} {self.bottom} {self.top}")

        self.enemy = Mob(Texs.BALL, 128, 128)
        self.add_entity_to_list(self.enemy, self.entities)
        self.enemy.flying = True

        self.idle_texture = arcade.load_texture("Salami/spritesheet.png", TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE, TILE_SIZE)
        self.idle_texture_mirrored = arcade.load_texture("Salami/spritesheet.png", TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE, TILE_SIZE, mirrored=True)
        self.walking_textures = Texs.load_textures("Salami/spritesheet.png", 4, 2, TILE_SIZE, 3)
        self.walking_textures_mirrored = Texs.load_textures("Salami/spritesheet.png", 4, 2, TILE_SIZE, 3, mirrored=True)

        self.walk_count = 0
        self.walk_frame_speed = 12
        self.player_dir = True

        self.player = Mob(Texs.BALL, 64, 64)
        self.add_entity_to_list(self.player, self.entities)

        level_gen_x = self.player.center_x // TILE_SIZE // ROOM_WIDTH
        level_gen_y = self.player.center_y // TILE_SIZE // ROOM_HEIGHT

        LevelGenerator.generateLevel(self, int(level_gen_x), int(level_gen_y))
        
        self.ball = Ball(Texs.BALL, self.player.center_x, self.player.center_y)
        self.ball.change_x = 2
        self.add_entity_to_list(self.ball, self.entities)

        self.engine = Engine(self.entities, self.tile_list, GRAVITY)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tile_list, GRAVITY)

        self.count = 0

    def update(self, delta):

        if self.keyboard.is_pressed("dash"):
            level_gen_x = self.player.center_x // TILE_SIZE // ROOM_WIDTH
            level_gen_y = self.player.center_y // TILE_SIZE // ROOM_HEIGHT

            LevelGenerator.generateLevel(self, int(level_gen_x), int(level_gen_y))

        if self.keyboard.is_pressed("attack"):
            self.ball.center_x = self.player.center_x
            self.ball.center_y = self.player.center_y
            self.ball.change_x = self.player.change_x * 8
            self.ball.change_y = self.player.change_y * 8

        if self.keyboard.is_pressed("jump"):
            if self.physics_engine.can_jump(1):
                self.physics_engine.jump(self.jump_height)
                self.jumping = True
            elif self.physics_engine.can_jump(-1):
                self.jumping = False
                self.curr_jump_height = 0
                
            if self.curr_jump_height > self.max_jump_height:
                self.jumping = False
                self.curr_jump_height = 0

        elif (self.curr_jump_height >= self.min_jump_height):
            self.jumping = False
            self.curr_jump_height = 0
        
        if self.jumping:
            self.player.change_y = self.jump_height
            self.curr_jump_height += self.jump_height

        speed_mult = 3
        if self.keyboard.is_pressed("sprint"):
            speed_mult = 1

        if self.keyboard.is_pressed("left"):
            self.player.change_x = -self.movespeed * speed_mult
        elif self.keyboard.is_pressed("right"):
            self.player.change_x = self.movespeed * speed_mult
        else:
            if self.player.change_x > 0:
                self.player.change_x -= 1
            elif self.player.change_x < 0:
                self.player.change_x += 1

        self.walk_count += 1
        if self.walk_count >= len(self.walking_textures) * self.walk_frame_speed:     
            self.walk_count = 0
        if self.player.change_x > 0:
            self.player.texture = self.walking_textures[self.walk_count // self.walk_frame_speed]
            self.player_dir = True

        elif self.player.change_x < 0:
            frame = self.walk_count // self.walk_frame_speed
            self.player.texture = self.walking_textures_mirrored[frame]
            self.player_dir = False
        else:
            if self.player_dir:
                self.player.texture = self.idle_texture
            else:
                self.player.texture = self.idle_texture_mirrored

        self.engine.update(delta)

        self.count += 1

    def draw(self):
        
        self.tile_list.draw(filter=gl.GL_NEAREST)
        self.entities.draw(filter=gl.GL_NEAREST)

        # self.player.draw_hit_box(arcade.color.BLUE)

    def add_entity_to_list(self, entity, list):
        entity.set_hit_box(SQUARE_HIT_BOX)
        entity.set_level(self)
        list.append(entity)

    def add_tile(self, tile):
        tile.set_hit_box(SQUARE_HIT_BOX)
        tile.set_level(self)
        self.set_tile(tile.center_x // TILE_SIZE, tile.center_y // TILE_SIZE, tile)

    def set_tile(self, x, y, tile):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        if self.tiles[(x, y)]:
            self.tile_list.remove(self.tiles[(x, y)])
        self.tile_list.append(tile)
        self.tiles[(x, y)] = tile

    def get_tiles(self, x, y, width, height):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        if self.tiles.get((x, y)):
            return self.tiles.get((x, y))
        return None

