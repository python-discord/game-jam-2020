import random

import arcade

from triple_vision.constants import (
    SCALED_TILE,
    SCALING,
    WINDOW_SIZE
)
from triple_vision.player import Player
from triple_vision.enemies import ChasingEnemy, Enemies


class TripleVision(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        self.tiles = None
        self.player = None
        self.enemy = None

        self.physics_engine = None

    def setup(self) -> None:
        self.tiles = arcade.SpriteList()

        for y in range(0, WINDOW_SIZE[1], SCALED_TILE):
            for x in range(0, WINDOW_SIZE[0], SCALED_TILE):
                self.tiles.append(
                    arcade.Sprite(
                        filename=f'assets/dungeon/frames/floor_{random.randint(1, 8)}.png',
                        scale=SCALING,
                        center_x=x + SCALED_TILE / 2,
                        center_y=y + SCALED_TILE / 2
                    )
                )

        self.player = Player('m')
        self.enemy = ChasingEnemy(Enemies.big_demon, self.player, 1, 50, center_x=50, center_y=500)

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.W:
            self.player.change_y = 5
        if key == arcade.key.S:
            self.player.change_y = -5
        if key == arcade.key.A:
            self.player.change_x = -5
        if key == arcade.key.D:
            self.player.change_x = 5

    def on_key_release(self, key, modifiers) -> None:
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_draw(self) -> None:
        self.tiles.draw()
        self.player.draw()
        self.enemy.draw()

    def on_update(self, delta_time: float) -> None:
        self.player.update_animation(delta_time)
        self.player.update()
        self.enemy.update()
