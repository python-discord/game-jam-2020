import arcade
import constants
import maths


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(
            constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT, constants.WINDOW_TITLE
        )

        arcade.set_background_color(constants.BACKGROUND_COLOR)

        self.player = arcade.Sprite("block.png", 1)
        self.player.center_x = constants.WINDOW_WIDTH // 2
        self.player.center_y = constants.WINDOW_HEIGHT // 2

        # FIXME: Get proper coords
        self.curr_mouse = (301, 301)

    def on_draw(self):
        """Draws all state to the screen"""
        arcade.start_render()

        self.player.draw()

    def update(self, delta_time):
        """Updates the internal state."""
        curr_pos = (self.player.center_x, self.player.center_y)
        (dx, dy) = maths.move_towards(self.curr_mouse, curr_pos, delta_time)
        self.player.center_x += dx
        self.player.center_y += dy

    def on_mouse_motion(self, x, y, _dx, _dy):
        self.curr_mouse = (x, y)
