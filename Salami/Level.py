
import arcade
import pyglet.gl as gl
import random
import PIL

import LevelGenerator
import Maths

from Textures import Textures

from Engine import Engine
from Entity import Entity, Texs
from Mob import Mob
from Ball import Ball
from Tile import Tile

from Constants import WIDTH, HEIGHT, TILE_SIZE, GRAVITY, SQUARE_HIT_BOX


class Level:

    def __init__(self, camera, keyboard):

        self.camera = camera
        self.keyboard = keyboard

        self.tile_list = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.entities = arcade.SpriteList()
        self.tiles = {}

        self.width = WIDTH // TILE_SIZE
        self.height = HEIGHT // TILE_SIZE

        self.movespeed = 2
        self.jump_height = 4
        self.jumping = False

        self.curr_jump_height = 0
        self.min_jump_height = 16
        self.max_jump_height = 32

        LevelGenerator.generateLevel(self)

        # for i in range(100):
        #     ball = Ball(Texs.BALL, 128 + 128 * random.random(), 128 + 128 * random.random())
        #     ball.change_x = random.randint(-8, 8)
        #     ball.change_y = random.randint(-8, 8)
        #     self.add_entity_to_list(ball, self.entities)

        # print(f"{self.left} {self.right} {self.bottom} {self.top}")

        self.enemy = Mob(Texs.BALL, 128, 128)
        self.add_entity_to_list(self.enemy, self.entities)
        self.enemy.flying = True

        self.idle_texture = 0

        self.idle_texture = arcade.load_texture("Salami/spritesheet.png", 0, TILE_SIZE * 3, TILE_SIZE, TILE_SIZE)
        self.idle_texture_mirrored = arcade.load_texture("Salami/spritesheet.png", 0, TILE_SIZE * 3, TILE_SIZE, TILE_SIZE, mirrored=True)
        self.walking_textures = Texs.load_textures("Salami/spritesheet.png", 0, 3, TILE_SIZE, 6)
        self.walking_textures_mirrored = Texs.load_textures("Salami/spritesheet.png", 0, 3, TILE_SIZE, 6, mirrored=True)

        self.walk_count = 0
        self.walk_frame_speed = 5
        self.player_dir = True

        self.player = Mob(Texs.BALL, 64, 64)
        self.add_entity_to_list(self.player, self.entities)

        self.engine = Engine(self.entities, self.tile_list, GRAVITY)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tile_list, GRAVITY)

        self.count = 0

    def update(self, delta):

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

        if self.keyboard.is_pressed("left"):
            self.player.change_x = -self.movespeed
        elif self.keyboard.is_pressed("right"):
            self.player.change_x = self.movespeed
        else:
            if self.player.change_x > 0:
                self.player.change_x -= 1
            elif self.player.change_x < 0:
                self.player.change_x += 1

        self.walk_count += 1
        if self.walk_count >= len(self.walking_textures) * self.walk_frame_speed:     
            self.walk_count = 0
        if self.player.change_x > 0:
            self.player.texture = self.walking_textures_mirrored[self.walk_count // self.walk_frame_speed]
            self.player_dir = True

        elif self.player.change_x < 0:
            frame = self.walk_count // self.walk_frame_speed
            self.player.texture = self.walking_textures[frame]
            # self.player.texture = self.walking_textures_mirrored[self.walk_count // self.walk_frame_speed]
            self.player_dir = False
        else:
            if self.player_dir:
                self.player.texture = self.idle_texture_mirrored
            else:
                self.player.texture = self.idle_texture

        self.engine.update(delta)

        if self.count % 30 == 0:
            tile = Tile(Texs.ROCK_TILE, random.randint(0, 49) * TILE_SIZE, random.randint(0, 49) * TILE_SIZE)
            self.add_entity_to_list(tile, self.tile_list)

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
        self.tile_list.append(tile)
        self.tiles[(x, y)] = tile

    def get_tiles(self, x, y, width, height):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        if self.tiles.get((x, y)):
            return self.tiles.get((x, y))
        return None

