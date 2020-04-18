from menuscreen import MenuView
from arcade.gui import *

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Main Menu")

    window.WINDOW_WIDTH = WINDOW_WIDTH
    window.WINDOW_HEIGHT = WINDOW_HEIGHT

    menu_view = MenuView()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
