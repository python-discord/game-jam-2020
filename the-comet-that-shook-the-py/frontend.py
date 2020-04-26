"""
Frontend of the 3x3 puzzle game
"""
from typing import (
    Optional,
    List,
    Tuple,
    Set,
)
import time

import arcade

from backend import start_new_game, check_results

# TODO fix this bad way of using constants for everything
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
(TILE_WIDTH, TILE_HEIGHT,) = (
    90,
    90,
)
TILE_PADDING_H = TILE_WIDTH // 2
TILE_PADDING_V = 10

TEXT_LEFT = WINDOW_HEIGHT * 2 / 3 + 200
TEXT_TOP = WINDOW_HEIGHT


class GridCell:
    """Represents a cell within the main grid which the user interacts with"""

    def __init__(self, centre: Tuple[float, float,], width, height, allowed_tile_values: Set[str]):
        self.bottom_left = (
            centre[0] - width / 2,
            centre[1] - height / 2,
        )
        self.top_right = (
            centre[0] + width / 2,
            centre[1] + height / 2,
        )
        self.centre = centre
        self.associated_tile: Optional[TileSprite] = None
        self.allowed_tile_values = allowed_tile_values

    def accept_tile(self, possible_tile: "TileSprite"):
        if possible_tile.tile_value not in self.allowed_tile_values:
            return False
        return True

    def place_associated_tile(self):
        self.associated_tile.center_x, self.associated_tile.center_y = self.centre
        self.associated_tile.set_bounds()

    def __repr__(self,):
        return str(self.centre)


class Button(arcade.Sprite):
    def __init__(self, asset_fp: str, centre):
        super(Button, self).__init__(asset_fp)
        self.center_x, self.center_y = centre

    def on_click(self):
        pass


class ClueTextBox(arcade.Sprite):
    """
    The textbox for showing clues
    """

    def __init__(self, clues):
        super(ClueTextBox, self).__init__("assets/background.png")
        self.clues = clues
        self.top, self.left = 900, 800
        self.width = WINDOW_WIDTH * 1 / 3 + 100
        self.height = WINDOW_HEIGHT * 0.7

    def draw(self):
        super(ClueTextBox, self).draw()
        size = 20 if len(self.clues) <= 10 else 16
        clue_text = "\n\n".join(self.clues)
        arcade.draw_text(
            clue_text,
            self.center_x,
            self.top - 110,
            arcade.color.BLACK,
            size,
            anchor_x="center",
            anchor_y="top",
            font_name="GARA",
        )


class TileSprite(arcade.Sprite):
    """
    The sprite that represents a movable tile.
    It can live either in the boneyard, or the submission grid.
    """

    def __init__(
        self, image_filepath: str, starting_x: int, starting_y: int,
    ):
        super().__init__(image_filepath)
        self.tile_value = image_filepath.split("/")[1]
        self.starting_x = starting_x
        self.starting_y = starting_y

        self.center_x = starting_x
        self.center_y = starting_y

        # TODO figure out the right scaling setup for these values
        self.width = TILE_WIDTH
        self.height = TILE_HEIGHT
        self.set_bounds()

    def set_bounds(self,):
        """
        Set boundary_left etc to be updated for a new center position
        """
        self.boundary_left = self.center_x - (self.width // 2)
        self.boundary_right = self.center_x + (self.width // 2)
        self.boundary_bottom = self.center_y - (self.height // 2)
        self.boundary_top = self.center_y + (self.height // 2)

    def reset(self,):
        """Resets the sprite back to its original starting position"""
        self.center_x = self.starting_x
        self.center_y = self.starting_y
        self.set_bounds()


class SubmissionGrid(arcade.Sprite):
    """
    The sprite representing the main game grid.
    """

    def __init__(self, allowed_values: List[str]):
        super().__init__("assets/grid.png")
        self.width = WINDOW_HEIGHT * (2 / 3)
        self.height = WINDOW_HEIGHT * (2 / 3)
        self.center_y = WINDOW_HEIGHT * (2 / 3) - (1 / 27 * WINDOW_HEIGHT)
        self.center_x = WINDOW_HEIGHT * 1 / 3 + WINDOW_HEIGHT * 1 / 27
        self.cells: List[GridCell] = []
        self._load_cells(allowed_values)

    def _load_cells(self, allowed_values):
        """
        Load the positions of all the cells
        """
        top_left = (
            self.center_x - self.width / 2,
            self.center_y + self.height / 2,
        )
        cell_width = self.width // 3
        cell_height = self.height // 3
        for row_num in range(3):
            for col_num in range(3):
                x = top_left[0] + (col_num * cell_width) + cell_width // 2
                y = top_left[1] - (row_num * cell_height) - cell_height // 2
                self.cells.append(
                    GridCell(
                        (x, y,),
                        cell_width,
                        cell_height,
                        allowed_values[row_num * 3 : (row_num + 1) * 3],
                    )
                )

    def get_relevant_cell(self, point: Tuple[float, float,],) -> GridCell:
        """
        Gets the cell, or None, in which the provided point resides
        :param point the x/y coord of which to check
        :return: Optionally, the relevant octothorpe cell
        """
        for cell in self.cells:
            if check_bounds(point, cell.bottom_left, cell.top_right,):
                return cell

    def extract_value(self,) -> List[Optional[str]]:
        """
        Extracts the values the player has inserted into
        the board into a format that can be used to verify the game
        :return: The list of strings representing the game state to be validated
        """
        return [
            cell.associated_tile.tile_value
            for cell in self.cells
            if cell.associated_tile is not None
        ]


class MyGame(arcade.Window):
    """
    Main Game Class
    """

    # TODO figure out how to render clues as text
    def __init__(self,):
        super().__init__(
            WINDOW_WIDTH, WINDOW_HEIGHT, "Fun",
        )
        self.submission_grid: Optional[SubmissionGrid] = None
        self.dragging_sprite: Optional[TileSprite] = None
        self.tile_sprites: Optional[arcade.SpriteList] = None
        self.button_list: Optional[arcade.SpriteList] = None
        self.clues: Optional[ClueTextBox] = None
        self.answers: Optional[List[str]] = None
        self.red_x: Optional[arcade.sprite] = None
        self._flash_red_x_end: Optional[int] = None
        self._red_x_visible = False
        arcade.set_background_color((100, 100, 100,))

    def setup(self,):
        """
        Set the game up for play. Call this to reset the game.
        """
        (answers, shuffled_list, clues, _,) = start_new_game()  # TODO, properly load the game
        self.clues = ClueTextBox(clues)
        self.answers = answers
        self.submission_grid = SubmissionGrid(answers)
        self.tile_sprites = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.red_x = arcade.Sprite("assets/red_x.png")
        timer = Button("assets/blank_button.png", (850, 110))
        done_button = Button("assets/done_button.png", (1130, 110))
        done_button.on_click = self.submit_game
        exit_button = Button("assets/exit_button.png", (1380 + 30, 110))
        self.button_list.extend([timer, done_button, exit_button])
        self.red_x.center_x, self.red_x.center_y = (
            self.submission_grid.center_x,
            self.submission_grid.center_y,
        )
        for ((x, y,), asset_path,) in zip(self.get_boneyard_starting_positions(), shuffled_list,):
            tile_sprite = TileSprite(f"assets/{asset_path}", int(x), int(y),)
            self.tile_sprites.append(tile_sprite)

    def on_draw(self,):
        """
        Main draw function. Draws the boneyard, and the submission grid.
        """
        arcade.start_render()
        self.submission_grid.draw()
        self.tile_sprites.draw()
        self.clues.draw()
        self.button_list.draw()
        if self._red_x_visible:
            self.red_x.draw()

    def update(self, delta_time):
        super(MyGame, self).update(delta_time)
        if not self._red_x_visible:
            return
        if time.time() > self._flash_red_x_end:
            self._red_x_visible = False

    def get_boneyard_starting_positions(self,):
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

    def on_mouse_motion(
        self, x, y, dx, dy,
    ):
        """ Called to update our objects. Happens approximately 60 times per second."""
        if self.dragging_sprite is not None:
            self.dragging_sprite.center_x = x
            self.dragging_sprite.center_y = y

    def on_mouse_press(
        self, x, y, button, modifiers,
    ):
        """
        Called when the user presses a mouse button.
        """
        for button in self.button_list:
            if check_bounds((x, y), (button.left, button.bottom), (button.right, button.top)):
                button.on_click()

        tile_sprite: TileSprite
        for tile_sprite in self.tile_sprites:
            if check_bounds(
                (x, y,),
                (tile_sprite.boundary_left, tile_sprite.boundary_bottom,),
                (tile_sprite.boundary_right, tile_sprite.boundary_top,),
            ):
                self.dragging_sprite = tile_sprite

    def on_mouse_release(
        self, x, y, button, modifiers,
    ):
        """
        Called when a user releases a mouse button.
        """

        if self.dragging_sprite is None:
            return

        grid_cell = self.submission_grid.get_relevant_cell((x, y,))
        if grid_cell is None:
            self.dragging_sprite.reset()
            self.dragging_sprite = None
            return

        if not grid_cell.accept_tile(self.dragging_sprite):
            self.dragging_sprite.reset()

            self.dragging_sprite = None
            return

        if grid_cell.associated_tile is not None:
            grid_cell.associated_tile.reset()
            grid_cell.associated_tile = None

        grid_cell.associated_tile = self.dragging_sprite
        grid_cell.place_associated_tile()
        self.dragging_sprite = None

    def submit_game(self):
        game_values = self.submission_grid.extract_value()
        if check_results(game_values, self.answers):
            self.handle_win()
        else:
            self.handle_incorrect_submission()

    def handle_win(self):
        print("You win")

    def handle_incorrect_submission(self):
        self._red_x_visible = True
        self._flash_red_x_end = time.time() + 1


def check_bounds(
    point: Tuple[float, float,], bottom_left: Tuple[float, float,], top_right: Tuple[float, float,],
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
