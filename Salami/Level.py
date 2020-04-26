
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
from EnemyBall import EnemyBall
from Enemy import Enemy
from Tile import Tile
from Slime import Slime
from Boss import Boss

from Constants import WIDTH, HEIGHT, \
    TILE_SIZE, GRAVITY, SQUARE_HIT_BOX, \
    ROOM_WIDTH, ROOM_HEIGHT

class Level:

    def __init__(self, camera, keyboard):

        self.camera = camera
        self.keyboard = keyboard

        self.width = WIDTH // TILE_SIZE
        self.height = HEIGHT // TILE_SIZE

        self.tile_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32, is_static=True)
        self.entities = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=64)
        self.particles = arcade.SpriteList(is_static=True)

        self.tiles = {}

        self.reset = False

        # for i in range(100):
        #     ball = Ball(Textures.get_texture(2, 5), 128 * random.random(), 128 * random.random())
        #     ball.change_x = random.randint(-8, 8)
        #     ball.change_y = random.randint(-8, 8)
        #     self.add_entity_to_list(ball, self.entities)

        self.player = Player(64, 64, self.keyboard)
        self.add_entity_to_list(self.player, self.entities)

        self.level_gen = LevelGenerator.LevelGen(self)
        self.paused = True
        self.difficulty = 1

        self.engine = Engine(self.entities, self.tile_list, self, GRAVITY)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tile_list, GRAVITY)

        self.curr_health = self.player.health

        self.health_bar = arcade.SpriteList()
        for i in range(3):
            heart = arcade.Sprite()
            heart.center_x = self.player.center_x - TILE_SIZE + i * TILE_SIZE
            heart.center_y = self.player.center_y - TILE_SIZE * 1.5
            heart.texture = Textures.get_texture(4, 9)
            self.health_bar.append(heart)

        self.setup()

    def setup(self):
    
        self.generate_level(self.player.center_x, self.player.center_y)
        # self.level_gen.rooms_to_draw.pop()

        self.title_sprite = Tile(Textures.TITLE_TEXTURE, 0, 0, False)
        self.flying = True
        self.title_sprite.center_x = TILE_SIZE * 10 + 8
        self.title_sprite.center_y = TILE_SIZE * 7 + 8
        self.add_tile(self.title_sprite)

    def update(self, delta):

        self.level_gen.update()

        if not (self.level_gen.generating or self.level_gen.drawing or self.paused):
            self.engine.update()

        if self.reset:
            self.difficulty += 1
            self.reset_level()
            self.generate_level(self.player.center_x, self.player.center_y)
            self.reset = False
        
        remainder = self.player.health if self.player.health > 0 else 0
        for i, health in enumerate(self.health_bar):
            health.center_x = self.player.center_x - TILE_SIZE + i * TILE_SIZE
            health.center_y = self.player.center_y - TILE_SIZE * 1.5
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
        self.particles.draw(filter=gl.GL_NEAREST)
        self.tile_list.draw(filter=gl.GL_NEAREST)

        self.health_bar.draw(filter=gl.GL_NEAREST)

        # self.player.draw_hit_box(arcade.color.BLUE)

    def add_entity_to_list(self, entity, list):
        entity.set_hit_box(SQUARE_HIT_BOX)
        entity.set_level(self)
        list.append(entity)

    def add_tile(self, tile):
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
        level_gen_x = int(x // TILE_SIZE // ROOM_WIDTH)
        level_gen_y = int(y // TILE_SIZE // ROOM_HEIGHT)
        
        self.level_gen.startGen(level_gen_x, level_gen_y)

        # LevelGenerator.generateLevel(self, int(level_gen_x), int(level_gen_y))

    def reset_level(self):
    
        self.tile_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32, is_static=True)
        # self.entities = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=64)
        self.tiles = {}
        # self.engine.tiles = self.tile_list
        # self.physics_engine.platforms = self.tile_list

        # self.add_entity_to_list(self.player, self.entities)

        for entity in self.entities:
            if entity == self.player:
                continue
            entity.removed = True

        # self.engine.update()
        # self.add_entity_to_list(self.player, self.entities)

        self.level_gen.rooms = {}
        self.level_gen.current_room = None
        self.level_gen.rooms_to_draw = []
        self.level_gen.generating = False
        self.level_gen.drawing = False
        self.level_gen.curr_generate_speed = 0
        self.level_gen.curr_draw_speed = 0