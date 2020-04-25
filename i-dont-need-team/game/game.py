import typing as t

import arcade

from .constants import BLOCK_HEIGHT, BLOCK_WIDTH, SCREEN_HEIGHT
from .utils import create_board, create_textures


class AdventuresGame(arcade.Window):
    """Adventures of 3 Balls main game class."""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.APPLE_GREEN)

        self.textures: t.List[arcade.Texture] = create_textures()

        self.board_sprite_list: t.Optional[arcade.SpriteList] = None
        self.road: t.Optional[t.List[t.List[int]]] = None

    def setup(self) -> None:
        """Setup/reset game state."""
        self.road = create_board()
        self.board_sprite_list = arcade.SpriteList()

        for row in range(len(self.road)):
            for column in range(len(self.road[0])):
                sprite = arcade.Sprite(scale=0.40)
                for texture in self.textures:
                    sprite.append_texture(texture)
                sprite.set_texture(self.road[row][column])
                sprite.center_x = BLOCK_WIDTH * column + BLOCK_WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - BLOCK_HEIGHT * row + BLOCK_HEIGHT // 2
                self.board_sprite_list.append(sprite)

    def on_draw(self) -> None:
        """Render game screen."""
        arcade.start_render()
        self.board_sprite_list.draw()
