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


class GridCell:
    def __init__(self, centre: Tuple[float, float], width, height):
        self.bottom_left = centre[0] - width / 2, centre[1] - height / 2
        self.top_right = centre[0] + width / 2, centre[1] + height / 2
        self.centre = centre

    def __repr__(self):
        return str(self.centre)


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
        self.set_bounds()

    def set_bounds(self):
        self.boundary_left = self.center_x - (self.width // 2)
        self.boundary_right = self.center_x + (self.width // 2)
        self.boundary_bottom = self.center_y - (self.height // 2)
        self.boundary_top = self.center_y + (self.height // 2)

    def reset(self):
        """Resets the sprite back to its original starting position"""
        self.center_x = self.starting_x
        self.center_y = self.starting_y


class SubmissionGrid(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/grid.png")
        self.width = WINDOW_HEIGHT * (2 / 3)
        self.height = WINDOW_HEIGHT * (2 / 3)
        self.center_y = WINDOW_HEIGHT * (2 / 3) - (1 / 27 * WINDOW_HEIGHT)
        self.center_x = WINDOW_HEIGHT * 1 / 3 + WINDOW_HEIGHT * 1 / 27
        self.cells: List[GridCell] = []
        self._load_grid()
        print(self.cells)

    def _load_grid(self):
        top_left = self.center_x - self.width / 2, self.center_y + self.height / 2
        cell_width = self.width // 3
        cell_height = self.height // 3
        for row_num in range(3):
            for col_num in range(3):
                x = top_left[0] + (col_num * cell_width) + cell_width // 2
                y = top_left[1] - (row_num * cell_height) - cell_height // 2
                print(x)
                self.cells.append(GridCell((x, y), cell_width, cell_height))

    def check_if_point_is_inside(self, point: Tuple[float, float]) -> Optional[Tuple[float, float]]:
        """
        Checks whether the provided point is within the octothorpe, if so, returns the coordinate of the subsection
        which that octothorpe belongs in
        :param point: the point to check the bounds of
        :return: None, or a point which is the centre of the octothorpe section which the provided point is in
        """
        for cell in self.cells:
            if check_bounds(point, cell.bottom_left, cell.top_right):
                return cell.centre


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
        self.submission_grid = SubmissionGrid()
        self.dragging_sprite: Optional[TileSprite] = None
        self.main_sprites: Optional[arcade.SpriteList] = None
        self.tile_sprites: Optional[arcade.SpriteList] = None

        arcade.set_background_color((100, 100, 100))

    def setup(self):
        """
        Set the game up for play. Call this to reset the game.
        """
        self.main_sprites = arcade.SpriteList()
        self.tile_sprites = arcade.SpriteList()
        for x, y in self.get_boneyard_starting_positions():
            # TODO interface this with the backend
            tile_sprite = TileSprite("assets/R3_watermelon_0.png", int(x), int(y))
            self.tile_sprites.append(tile_sprite)

    def get_boneyard_starting_positions(self):
        """
        yields the positions where tiles should be placed in the starting boneyard
        """
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
        self.submission_grid.draw()
        self.tile_sprites.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        if self.dragging_sprite is not None:
            self.dragging_sprite.center_x = x
            self.dragging_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        tile_sprite: TileSprite
        for tile_sprite in self.tile_sprites:
            if check_bounds(
                (x, y),
                (tile_sprite.boundary_left, tile_sprite.boundary_bottom),
                (tile_sprite.boundary_right, tile_sprite.boundary_top),
            ):
                self.dragging_sprite = tile_sprite

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        if self.dragging_sprite is not None:
            print(x, y)
            print(self.submission_grid.check_if_point_is_inside((x, y)))
            if (point := self.submission_grid.check_if_point_is_inside((x, y))) is not None:
                print("stuff")
                self.dragging_sprite.center_x = point[0]
                self.dragging_sprite.center_y = point[1]
            else:
                self.dragging_sprite.reset()
            self.dragging_sprite = None


def check_bounds(
    point: Tuple[float, float], bottom_left: Tuple[float, float], top_right: Tuple[float, float],
) -> bool:
    """
    Check if a given point is within the bounds of 4 sides
    :param top_right: the top right of the bounding rectangle
    :param bottom_left: the bottom left of the bounding rectangle
    :param point: x/y coords of a point to check
    :return: True/False
    """
    if bottom_left == top_right:
        raise ValueError("Bottom left and top right can't be the same")
    return (bottom_left[0] < point[0] < top_right[0]) and (bottom_left[1] < point[1] < top_right[1])
