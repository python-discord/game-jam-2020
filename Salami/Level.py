
import arcade
import pyglet.gl as gl

import Engine
import Entity

from Constants import WIDTH, HEIGHT, TILE_SIZE, GRAVITY, SQUARE_HIT_BOX


class Level:

    def __init__(self, camera, keyboard):

        self.camera = camera
        self.keyboard = keyboard

        self.tiles = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        self.entities = arcade.SpriteList()

        self.movespeed = 5
        self.jumpheight = 5

        for x in range(0, WIDTH // TILE_SIZE, TILE_SIZE):
            tile = Entity.Entity(Entity.ROCK_TILE, x + 32, 48)
            tile.set_hit_box(SQUARE_HIT_BOX)
            self.tiles.append(tile)

        for y in range(TILE_SIZE, TILE_SIZE * 4, TILE_SIZE):
            tile = Entity.Entity(Entity.ROCK_TILE, 0, y)
            tile.set_hit_box(SQUARE_HIT_BOX)
            self.tiles.append(tile)
        
        for x in range(0, WIDTH, TILE_SIZE):
            tile = Entity.Entity(Entity.ROCK_TILE, x, 0)
            tile.set_hit_box(SQUARE_HIT_BOX)
            self.tiles.append(tile)

        self.player = Entity.Entity(Entity.PLAYER, 64, 64)
        self.player.set_hit_box(SQUARE_HIT_BOX)
        self.entities.append(self.player)

        print(self.player.get_hit_box())
        print(self.tiles[0].get_hit_box())

        # print(f"Top: {self.player.top} | Left: {self.player.right}")
        # print(f"Bottom: {self.player.top} | Right: {self.player.right}")
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tiles, GRAVITY)

    def update(self, delta):

        if self.keyboard.is_pressed("up") and self.physics_engine.can_jump(1):
            self.physics_engine.jump(self.jumpheight)

        if self.keyboard.is_pressed("left"):
            self.player.change_x = -self.movespeed
        elif self.keyboard.is_pressed("right"):
            self.player.change_x = self.movespeed
        else:
            self.player.change_x = 0
            
        self.physics_engine.update()

    def draw(self):
        self.tiles.draw(filter=gl.GL_NEAREST)
        self.entities.draw(filter=gl.GL_NEAREST)

        # for tile in self.tiles:
        #     tile.draw_hit_box(arcade.color.RED)

        # self.player.draw_hit_box(arcade.color.BLUE)