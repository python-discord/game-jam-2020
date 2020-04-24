from typing import Optional, List, Tuple

import arcade

# TODO fix this bad way of using constants for everything
BOARD_SIZE = 3
SQUARE_SIZE = 200
MARGIN = 10
TEXT_SIZE = 50
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
TILE_WIDTH, TILE_HEIGHT = 90, 90  # WINDOW_WIDTH/32, WINDOW_WIDTH/32
TILE_PADDING_H = TILE_WIDTH // 2
TILE_PADDING_V = 10


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
        self.boundary_left = (self.center_x - (self.width // 2))
        self.boundary_right = self.center_x + (self.width // 2)
        self.boundary_bottom = self.center_y - (self.height // 2)
        self.boundary_top = self.center_y + (self.height // 2)


class SubmissionGrid(arcade.Sprite):

    def __init__(self):
        super().__init__('assets/grid.png')
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
        self.main_sprites = arcade.SpriteList()
        self.main_sprites.append(SubmissionGrid())
        self.tile_sprites = arcade.SpriteList()
        for x, y in self.get_boneyard_starting_positions():
            tile_sprite = TileSprite('assets/R3_watermelon_0.png', int(x), int(y))
            self.tile_sprites.append(tile_sprite)

    def get_boneyard_starting_positions(self):
        for i in range(9):
            left_edge_padding = 1 / 27 * WINDOW_WIDTH
            tile_and_padding = ((TILE_WIDTH * i) + TILE_PADDING_H * i) // 2
            if i % 2 == 0:
                tile_height = TILE_HEIGHT * 2 + TILE_PADDING_V
            else:
                tile_height = TILE_HEIGHT
            yield left_edge_padding + tile_and_padding, tile_height

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
        tile_sprite: TileSprite
        for tile_sprite in self.tile_sprites:

            if check_bounds(
                    (x, y),
                    (tile_sprite.boundary_left, tile_sprite.boundary_bottom),
                    (tile_sprite.boundary_right, tile_sprite.boundary_top)):
                print(
                    f'{x, y} is within the bounds of {(tile_sprite.boundary_left, tile_sprite.boundary_bottom)} and {(tile_sprite.boundary_right, tile_sprite.boundary_top)}')


def check_bounds(point: Tuple[float, float],
                 bottom_left: Tuple[float, float],
                 top_right: Tuple[float, float]) -> bool:
    """
    Check if a given point is within the bounds of 4 sides
    :param top_right: the top right of the bounding rectangle
    :param bottom_left: the bottom left of the bounding rectangle
    :param point: x/y coords of a point to check
    :return: True/False
    """
    return False
    # if bottom_left == top_right:
    #     raise ValueError("Bottom left and top right can't be the same")
    # return point[0] > bottom_left[0] and point[1] > bottom_left[1] and point[0] < top_right[0] and point[1] > top_right[
    #     1]
