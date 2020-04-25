import copy
import typing as t

import arcade

from .constants import Blocks, BLOCK_HEIGHT, BLOCK_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, BLOCKS_AMOUNT_X
from .utils import create_board, create_textures


class AdventuresGame(arcade.Window):
    """Adventures of 3 Balls main game class."""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.APPLE_GREEN)

        self.textures: t.List[arcade.Texture] = create_textures()

        self.board_sprite_list: t.Optional[arcade.SpriteList] = None
        self.balls: t.Optional[arcade.SpriteList] = None
        self.road: t.Optional[t.List[t.List[int]]] = None
        self.frames: t.Optional[arcade.SpriteList] = None

    def setup(self) -> None:
        """Setup/reset game state."""
        self.road = create_board()
        self.board_sprite_list = arcade.SpriteList()
        self.balls = arcade.SpriteList()
        self.frames = arcade.SpriteList()

        for row in range(len(self.road)):
            for column in range(len(self.road[0])):
                sprite = arcade.Sprite(scale=0.40)
                for texture in self.textures:
                    sprite.append_texture(texture)
                sprite.set_texture(self.road[row][column])
                sprite.center_x = (BLOCK_WIDTH * column) + BLOCK_WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - BLOCK_HEIGHT * row + BLOCK_HEIGHT // 2
                self.board_sprite_list.append(sprite)
                if self.road[row][column] == Blocks.frame:
                    self.frames.append(sprite)

        pos = (4, 8, 12)

        for i, col in enumerate(("red_ball", "blue_ball", "green_ball")):
            s = arcade.Sprite(f"./resources/{col}.png", scale=0.40)
            s.position = (pos[i] * BLOCK_WIDTH, SCREEN_HEIGHT / 4)
            self.balls.append(s)

    def on_draw(self) -> None:
        """Render game screen."""
        arcade.start_render()
        self.board_sprite_list.draw()
        self.balls.draw()

    def move(self, direction: int) -> None:
        """Move balls based on direction. `-1` is left and `1` right."""
        status = []
        for ball in self.balls:
            s = copy.deepcopy(ball)
            s.center_x += BLOCK_WIDTH * direction
            if not arcade.check_for_collision_with_list(s, self.frames):
                status.append(True)
                continue
            status.append(False)
        yes = all(s for s in status)
        if yes:
            for ball in self.balls:
                ball.center_x += BLOCK_WIDTH * direction

    def on_key_press(self, key, _) -> None:
        """Handle key pressing."""
        if key == arcade.key.LEFT:
            self.move(-1)
        elif key == arcade.key.RIGHT:
            self.move(1)

