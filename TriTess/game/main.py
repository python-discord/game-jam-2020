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
import arcade

# Set how many rows and columns we will have
from TriTess.game import trigrid


BOARD_SIZE = 12

# This sets the WIDTH of each grid location
WIDTH = 50

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * BOARD_SIZE + MARGIN
SCREEN_HEIGHT = SCREEN_WIDTH
CELL_WIDTH = int(SCREEN_WIDTH/BOARD_SIZE)

SCREEN_TITLE = "TriTess Grid example"


class TriTess(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """

        super().__init__(width, height, title)
        self.trigrid = trigrid.TriGrid(BOARD_SIZE, CELL_WIDTH, 'triangular')
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
        x, y, r = self.trigrid.get_grid_position(coord_x, coord_y)
        print(f"Click coordinates: ({coord_x}, {coord_y}). Grid coordinates: ({x}, {y}, {r})")

        if button == arcade.MOUSE_BUTTON_LEFT:
            self.trigrid.toggle_cell(x, y, r)
            self.trigrid.update_shape_list()
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.trigrid.toggle_cell(x, y, r)
            neighbor_list = self.trigrid.get_grid_neighbor(coord_x, coord_y)
            for neighbor in neighbor_list:
                self.trigrid.toggle_cell(*neighbor)

        self.trigrid.update_shape_list()
        self.on_draw()


def main():
    tritess_window = TriTess(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()