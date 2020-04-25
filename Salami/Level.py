
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
        # self.player.flying = False
        self.add_entity_to_list(self.player, self.entities)

        self.level_gen = LevelGenerator.LevelGen(self)

        self.generate_level(self.player.x, self.player.y)

        # rooms = [(0, 0, 1), (1, 1, 1), (2, 2, 1), (3, 3, 1)]
        # for i, room in enumerate(rooms):
        #     LevelGenerator.generateRoom(self,
        #         room[0] * ROOM_WIDTH + room[0],
        #         room[1] * ROOM_HEIGHT + room[1], room[2])
        
        self.ball = Ball(Textures.SPRITESHEET[2 + 5 * 16], self.player.center_x, self.player.center_y)
        self.ball.change_x = 2
        self.add_entity_to_list(self.ball, self.entities)

        self.engine = Engine(self.entities, self.tile_list, self, GRAVITY)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tile_list, GRAVITY)

        self.curr_health = self.player.health

        self.health_bar = arcade.SpriteList()
        for i in range(3):
            heart = arcade.Sprite()
            heart.center_x = self.player.center_x - TILE_SIZE + i * TILE_SIZE
            heart.center_y = self.player.center_y + TILE_SIZE
            heart.texture = Textures.get_texture(4, 9)
            self.health_bar.append(heart)

    def update(self, delta):

        # e = Entity(Texs.ROCK_TILE, 0, 0)

        # self.add_entity_to_list(e, self.entities)

        # e.level = None
        # self.entities.remove(e)
        self.level_gen.update()

        self.engine.update(delta)
        
        remainder = self.player.health if self.player.health > 0 else 0
        for i, health in enumerate(self.health_bar):
            health.center_x = self.player.center_x - TILE_SIZE + i * TILE_SIZE
            health.center_y = self.player.center_y + TILE_SIZE
            if self.player.health < self.curr_health:
                if remainder >= 3:
                    health.texture = Textures.get_texture(4, 9)
                    remainder -= 3
                else:
                    health.texture = Textures.get_texture(4 + 3 - remainder, 9)
                    remainder = 0
        self.curr_health = self.player.health

    def draw(self):
        
        self.entities.draw(filter=gl.GL_NEAREST)
        self.tile_list.draw(filter=gl.GL_NEAREST)

        self.health_bar.draw(filter=gl.GL_NEAREST)

        self.player.draw_hit_box(arcade.color.BLUE)

    def add_entity_to_list(self, entity, list):
        entity.set_hit_box(SQUARE_HIT_BOX)
        entity.set_level(self)
        list.append(entity)

    def add_tile(self, tile):
        print(f"{tile.left}, {tile.bottom}, {tile.width}")
        # tile.set_hit_box(SQUARE_HIT_BOX)
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

    def generate_level(self, x, y):
        level_gen_x = int(x / TILE_SIZE / ROOM_WIDTH)
        level_gen_y = int(x / TILE_SIZE / ROOM_HEIGHT)
        
        # self.level_gen.startGen(level_gen_x, level_gen_y)

        LevelGenerator.generateLevel(self, int(level_gen_x), int(level_gen_y))