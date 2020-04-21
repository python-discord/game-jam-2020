from typing import Optional

import arcade

# Colors
BACKGROUND_COLOR = 119, 110, 101
EMPTY_CELL = 205, 193, 180
TEXT_COLOR_DARK = 119, 110, 101
TEXT_COLOR_LIGHT = 249, 246, 242
SQUARE_COLORS = (200, 0, 0), \
                (238, 228, 218), \
                (237, 224, 200), \
                (242, 177, 121), \
                (245, 149, 99), \
                (246, 124, 95), \
                (246, 94, 59), \
                (237, 207, 114), \
                (237, 204, 97), \
                (237, 200, 80), \
                (237, 197, 63), \
                (237, 194, 46), \
                (62, 57, 51)

# Sizes
BOARD_SIZE = 3
SQUARE_SIZE = 200
MARGIN = 10
TEXT_SIZE = 50
WINDOW_WIDTH = 1920  # BOARD_SIZE * (SQUARE_SIZE + MARGIN) + MARGIN
WINDOW_HEIGHT = 1080  # BOARD_SIZE * (SQUARE_SIZE + MARGIN) + MARGIN
TILE_WIDTH, TILE_HEIGHT = (WINDOW_WIDTH / 12, WINDOW_HEIGHT / 12)
TILE_PADDING = 0  # (WINDOW_WIDTH/16)*0.01
# Font
FONT = "arial.ttf"


class TileSprite(arcade.Sprite):
    def __init__(self, image_filepath: str, starting_x: int, starting_y: int):
        super().__init__(image_filepath)
        self.starting_x = starting_x
        self.starting_y = starting_y

        self.center_x = starting_x
        self.center_y = starting_y
        self.width = 100
        self.height = 100


class SubmissionGrid(arcade.Sprite):
    def __init__(self):
        super().__init__('frontend/sprites/grid.png')
        self.width = WINDOW_HEIGHT * (2 / 3)
        self.height = WINDOW_HEIGHT * (2 / 3)
        self.center_y = WINDOW_HEIGHT * (2 / 3) - (1 / 27 * WINDOW_HEIGHT)
        self.center_x = WINDOW_HEIGHT * 1 / 3 + WINDOW_HEIGHT * 1 / 27


class MyGame(arcade.Window):
    """
    Main Game Class
    """

    def __init__(self):
        """
        Initializer for MyGame
        """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "2048")
        self.main_sprites: Optional[arcade.SpriteList] = None
        self.tile_sprites: Optional[arcade.SpriteList] = None

        arcade.set_background_color((100, 100, 100))

        self.boneyard_starting_positions = (
            (1 / 27 * WINDOW_WIDTH + (TILE_WIDTH * i + TILE_PADDING * i) // 2,
             TILE_HEIGHT + TILE_HEIGHT * (i % 2))
            for i in range(9))

    def setup(self):
        """
        Set the game up for play. Call this to reset the game.
        :return:
        """
        self.main_sprites = arcade.SpriteList()
        self.main_sprites.append(SubmissionGrid())
        self.tile_sprites = arcade.SpriteList()
        for x, y in self.boneyard_starting_positions:
            self.tile_sprites.append(TileSprite('frontend/sprites/plum.png', int(x), int(y)))

    def on_draw(self):
        """
        Draw the grid
        :return:
        """
        arcade.start_render()
        self.main_sprites.draw()
        self.tile_sprites.draw()
