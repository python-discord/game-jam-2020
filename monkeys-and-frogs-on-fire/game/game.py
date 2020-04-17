import random

import arcade

from game.constants import (
    SCALED_TILE,
    SCALING,
    WINDOW_SIZE
)
from game.player import Player


class Game(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        self.tiles = None
        self.player = None

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

    def on_draw(self) -> None:
        self.tiles.draw()
        self.player.draw()

    def on_update(self, delta_time: float) -> None:
        self.player.update_animation(delta_time)
