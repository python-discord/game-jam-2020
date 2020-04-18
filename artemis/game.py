import arcade
import random
import math

from constants import WIDTH, HEIGHT, SCALING, SIDE, TOP
from engine import BiDirectionalPhysicsEnginePlatformer
from player import Player
from sprites import Block, Gem
from displays import Box


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, 'Runner')
        arcade.set_background_color((25, 0, 50))

        # sprites
        self.player = Player(self)

        self.blocks = arcade.SpriteList()

        size = int(128 * SCALING)
        for x in range(-SIDE, WIDTH+SIDE, size):
            Block(self, x, HEIGHT - TOP)
            Block(self, x, size//2)

        self.gems = arcade.SpriteList()
        for _ in range(2):
            Gem(self)

        self.boxes = arcade.SpriteList()
        for n in range(5):
            Box(self, n)

        self.others = arcade.SpriteList()
        
        self.engine = BiDirectionalPhysicsEnginePlatformer(
            self.player, self.blocks, 1
        )

        # keep track of things
        self.pressed = []
        self.left = 0

        arcade.run()

    def on_draw(self):
        arcade.start_render()
        self.blocks.draw()
        self.gems.draw()
        self.boxes.draw()
        self.others.draw()
        self.player.draw()

    def on_update(self, timedelta):
        self.gems.update()
        self.blocks.update()
        self.player.update(timedelta)
        self.boxes.update()
        self.others.update()
        self.engine.update()
        self.scroll()

    def scroll(self):
        self.left += self.player.speed
        arcade.set_viewport(self.left, WIDTH + self.left, 0, HEIGHT)

    def on_key_press(self, key, modifiers):
        self.pressed.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.pressed:
            self.pressed.remove(key)