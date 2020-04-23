"""Run the actual game. This is the only file intended to be run directly."""
import arcade

from constants import BACKGROUND, HEIGHT, WIDTH
from views import Menu


window = arcade.Window(WIDTH, HEIGHT, 'Gem Matcher')
arcade.set_background_color(BACKGROUND)
window.show_view(Menu())
window.set_vsync(True)
arcade.run()
