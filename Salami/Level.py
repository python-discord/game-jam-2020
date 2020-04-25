
import arcade
import pyglet.gl as gl
import random
import PIL

import LevelGenerator
import Maths

import Textures

from Engine import Engine
from Entity import Entity, Texs, Tex
from Projectile import Projectile
from Mob import Mob
from Player import Player
from Ball import Ball
from Tile import Tile

from Constants import WIDTH, HEIGHT, \
    TILE_SIZE, GRAVITY, SQUARE_HIT_BOX, \
    ROOM_WIDTH, ROOM_HEIGHT

class Level:

    def __init__(self, camera, keyboard):

        self.camera = camera
        self.keyboard = keyboard

        self.width = WIDTH // TILE_SIZE
        self.height = HEIGHT // TILE_SIZE

        self.tile_list = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.entities = arcade.SpriteList()
        self.tiles = {}

        self.rooms = []

        # for i in range(100):
        #     ball = Ball(Textures.get_texture(2, 5), 128 * random.random(), 128 * random.random())
        #     ball.change_x = random.randint(-8, 8)
        #     ball.change_y = random.randint(-8, 8)
        #     self.add_entity_to_list(ball, self.entities)

        self.player = Player(Textures.SPRITESHEET[4 + 3 * 16], 64, 64, self.keyboard)
        self.add_entity_to_list(self.player, self.entities)

        level_gen_x = self.player.center_x // TILE_SIZE // ROOM_WIDTH
        level_gen_y = self.player.center_y // TILE_SIZE // ROOM_HEIGHT

        LevelGenerator.generateLevel(self, int(level_gen_x), int(level_gen_y))

        # rooms = [(0, 0, 1), (1, 1, 1), (2, 2, 1), (3, 3, 1)]
        # for i, room in enumerate(rooms):
        #     LevelGenerator.generateRoom(self,
        #         room[0] * ROOM_WIDTH + room[0],
        #         room[1] * ROOM_HEIGHT + room[1], room[2])
        
        self.ball = Ball(Textures.SPRITESHEET[2 + 5 * 16], self.player.center_x, self.player.center_y)
        self.ball.change_x = 2
        self.add_entity_to_list(self.ball, self.entities)

        self.engine = Engine(self.entities, self.tile_list, GRAVITY)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tile_list, GRAVITY)

        self.count = 0

    def update(self, delta):

        # e = Entity(Texs.ROCK_TILE, 0, 0)

        # self.add_entity_to_list(e, self.entities)

        # e.level = None
        # self.entities.remove(e)

        self.engine.update(delta)

        self.count += 1

    def draw(self):
        
        self.entities.draw(filter=gl.GL_NEAREST)
        self.tile_list.draw(filter=gl.GL_NEAREST)

        self.camera.reset_viewport()
        # self.player.draw_hit_box(arcade.color.BLUE)

    def add_entity_to_list(self, entity, list):
        # entity.set_hit_box(SQUARE_HIT_BOX)
        entity.set_level(self)
        list.append(entity)

    def add_tile(self, tile):
        tile.set_hit_box(SQUARE_HIT_BOX)
        tile.set_level(self)
        self._set_tile(int(tile.center_x // TILE_SIZE), int(tile.center_y // TILE_SIZE), tile)

    def _set_tile(self, x: int, y: int, tile):
        # if x < 0 or y < 0 or x >= self.width or y >= self.height:
        #     return
        if self.tiles.get((x, y)):
            self.tile_list.remove(self.tiles[(x, y)])
        self.tile_list.append(tile)
        self.tiles[(x, y)] = tile
    
    def remove_tile(self, x: int, y: int):
        if self.tiles.get((x, y)):
            self.tile_list.remove(self.tiles[(x, y)])
            self.tiles.pop((x, y))

    def get_tile(self, x: int, y: int):
        # if x < 0 or y < 0 or x >= self.width or y >= self.height:
        #     return None
        if self.tiles.get((x, y)):
            return self.tiles.get((x, y))
        return None

    def get_tiles(self, x0: int, y0: int, x1: int, y1: int):
        list = []
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if self.get_tile(x, y):
                    list.append(self.get_tile(x, y))
        return list

