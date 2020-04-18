import random

import arcade

from triple_vision.constants import (
    SCALED_TILE,
    SCALING,
    WINDOW_SIZE
)
from triple_vision.entities import (
    ChasingEnemy,
    Enemies,
    Player
)


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
        self.enemy = ChasingEnemy(Enemies.big_demon, self.player, 1, SCALED_TILE * 10, center_x=50, center_y=500)

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.move_to(x, y, rotate=False)

    def on_draw(self) -> None:
        self.tiles.draw()
        self.player.draw()
        self.enemy.draw()

    def on_update(self, delta_time: float) -> None:
        self.player.update(delta_time)
        self.enemy.update()
