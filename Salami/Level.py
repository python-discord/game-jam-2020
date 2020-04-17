
import arcade
import pyglet.gl as gl

WIDTH = 600
HEIGHT = 400

TILE_SIZE = 16
GRAVITY = 0.2


class Level:

    def __init__(self, camera, keyboard):

        self.camera = camera
        self.keyboard = keyboard

        self.tiles = arcade.SpriteList()
        self.entities = arcade.SpriteList()

        self.movespeed = 5

        for x in range(0, WIDTH // TILE_SIZE, TILE_SIZE):
            tile = arcade.Sprite("Salami/spritesheet.png", 1, 0, 0, TILE_SIZE, TILE_SIZE)
            tile.left = x + 32
            tile.bottom = 48
            self.tiles.append(tile)

        for y in range(TILE_SIZE, TILE_SIZE * 4, TILE_SIZE):
            tile = arcade.Sprite("Salami/spritesheet.png", 1, 0, 0, TILE_SIZE, TILE_SIZE)
            tile.left = 0
            tile.bottom = y
            self.tiles.append(tile)
        
        for x in range(0, WIDTH, TILE_SIZE):
            tile = arcade.Sprite("Salami/spritesheet.png", 1, 0, 0, TILE_SIZE, TILE_SIZE)
            tile.left = x
            tile.bottom = 0
            self.tiles.append(tile)
        
        self.player = arcade.Sprite("Salami/spritesheet.png", 1, TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
        self.player.left = 64
        self.player.bottom = 64
        self.entities.append(self.player)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tiles, GRAVITY)

    def update(self, delta):

        if self.keyboard.is_pressed("up") and self.physics_engine.can_jump(1):
            self.physics_engine.jump(5)

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