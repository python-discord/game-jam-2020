import arcade
import pathlib
from .config import BACKGROUND_COLOR
from .maths import move_towards
from ...constants import WINDOW_WIDTH, WINDOW_HEIGHT


class BlockChaser(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        arcade.set_background_color(BACKGROUND_COLOR)

        sprite_path = pathlib.Path(__file__) / ".." / "block.png"
        self.player = arcade.Sprite(sprite_path, 1)
        self.player.center_x = WINDOW_WIDTH // 2
        self.player.center_y = WINDOW_HEIGHT // 2

        # FIXME: Get proper coords
        self.curr_mouse = (301, 301)

    def on_draw(self):
        """Draws all state to the screen"""
        arcade.start_render()

        self.player.draw()

    def update(self, delta_time):
        """Updates the internal state."""
        curr_pos = (self.player.center_x, self.player.center_y)
        (dx, dy) = move_towards(self.curr_mouse, curr_pos, delta_time)
        self.player.center_x += dx
        self.player.center_y += dy

    def on_mouse_motion(self, x, y, _dx, _dy):
        self.curr_mouse = (x, y)
