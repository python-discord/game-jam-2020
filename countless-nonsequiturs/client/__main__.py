import arcade
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from .views import InitialView

if __name__ == "__main__":
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    initial_view = InitialView()
    window.show_view(initial_view)
    arcade.run()
