"""
Array Backed Grid

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

Note: Regular drawing commands are slow. Particularly when drawing a lot of
items, like the rectangles in this example.

For faster drawing, create the shapes and then draw them as a batch.
See array_backed_grid_buffered.py

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid
"""
import os

import arcade

# Set how many rows and columns we will have
from TriTess.game import trigrid


BOARD_SIZE = 18

# This sets the WIDTH of each grid location
WIDTH = 40

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * BOARD_SIZE + MARGIN
SCREEN_HEIGHT = SCREEN_WIDTH
CELL_WIDTH = int(SCREEN_WIDTH/BOARD_SIZE)

SCREEN_TITLE = "TriTess Grid example"
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 1)[0], 'data')


class TriTess(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """

        super().__init__(width, height, title)
        self.trigrid = trigrid.TriGrid(BOARD_SIZE, CELL_WIDTH, 'trichess3')
        self.cur_player = 0
        self.cur_cell = None
        self.cur_valid_moves = None
        self.cur_valid_attacks = None

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the grid
        self.trigrid.on_draw(grid_coord=True)

    def on_mouse_press(self, coord_x, coord_y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        pos = self.trigrid.get_grid_position(coord_x, coord_y)
        if pos in self.trigrid.grid_map:
            print(f"Click coordinates: ({coord_x}, {coord_y}). Grid coordinates: ({pos})")

            if button == arcade.MOUSE_BUTTON_LEFT:
                self.trigrid.clear_highlights()
                self.cur_cell = self.trigrid.get_cell(*pos)
                if self.cur_cell.piece is not None and self.cur_cell.piece.player == self.cur_player:
                    self.cur_valid_attacks = self.cur_cell.piece.list_valid_attacks()
                    for attack in self.cur_valid_attacks:
                        self.trigrid.get_cell(*attack).set_highlight("attackable")

                    self.cur_valid_moves = self.cur_cell.piece.list_valid_moves()
                    for move in self.cur_valid_moves:
                        self.trigrid.get_cell(*move).set_highlight("movable")

                else:
                    self.clear_selection()

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                if self.cur_cell is not None:
                    new_cell = self.trigrid.get_cell(*pos)
                    if new_cell.piece is not None and self.cur_cell.piece.player != new_cell.piece.player:
                        if pos in self.cur_valid_attacks:
                            new_cell.piece.remove_from_sprite_lists()
                            new_cell.piece = None
                            self.cur_cell.piece.move_to(*pos)
                            self.cur_player = (self.cur_player + 1) % self.trigrid.num_players

                    elif pos in self.cur_valid_moves:
                        self.trigrid.get_cell(*pos).piece = self.cur_cell.piece

                        self.cur_cell.piece.move_to(*pos)
                        self.cur_player = (self.cur_player + 1) % self.trigrid.num_players

                    self.clear_selection()

            self.on_draw()

    def clear_selection(self):
        self.cur_cell = None
        self.cur_valid_moves = None
        self.cur_valid_attacks = None
        self.trigrid.clear_highlights()

def main():
    tritess_window = TriTess(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
