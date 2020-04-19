import arcade

from views import Menu
from constants import WIDTH, HEIGHT, BACKGROUND


window = arcade.Window(WIDTH, HEIGHT, 'Gem Matcher')
arcade.set_background_color(BACKGROUND)
window.show_view(Menu())
arcade.run()