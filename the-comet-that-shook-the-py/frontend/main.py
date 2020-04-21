from typing import Optional

import arcade

# TODO fix this bad way of using constants for everything
BOARD_SIZE = 3
SQUARE_SIZE = 200
MARGIN = 10
TEXT_SIZE = 50
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
TILE_WIDTH, TILE_HEIGHT = (WINDOW_WIDTH / 12, WINDOW_HEIGHT / 9)
TILE_PADDING = 0  # (WINDOW_WIDTH/16)*0.01


class TileSprite(arcade.Sprite):
    def __init__(self, image_filepath: str, starting_x: int, starting_y: int):
        super().__init__(image_filepath)
        self.starting_x = starting_x
        self.starting_y = starting_y

        self.center_x = starting_x
        self.center_y = starting_y

        # TODO figure out the right scaling setup for these values
        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT


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

    # TODO figure out how to render clues as text
    def __init__(self):
        """
        Initializer for MyGame
        """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "2048")
        self.main_sprites: Optional[arcade.SpriteList] = None
        self.tile_sprites: Optional[arcade.SpriteList] = None

        arcade.set_background_color((100, 100, 100))

    def setup(self):
        """
        Set the game up for play. Call this to reset the game.
        :return:
        """
        boneyard_starting_positions = (
            (1 / 27 * WINDOW_WIDTH + (TILE_WIDTH * i + TILE_PADDING * i) // 2,
             TILE_HEIGHT + TILE_HEIGHT * (i % 2))
            for i in range(9))
        self.main_sprites = arcade.SpriteList()
        self.main_sprites.append(SubmissionGrid())
        self.tile_sprites = arcade.SpriteList()
        for x, y in boneyard_starting_positions:
            self.tile_sprites.append(TileSprite('frontend/sprites/plum.png', int(x), int(y)))

    def on_draw(self):
        """
        Main draw function. Draws the boneyard, and the submission grid
        """
        arcade.start_render()
        self.main_sprites.draw()
        self.tile_sprites.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        # TODO add code that makes a tile track the mouse here

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # TODO add code that detects whether a mouseclick is within the bounds of a sprite

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        # TODO add code that locks a tile either into the boneyard, or into a slot on the board
