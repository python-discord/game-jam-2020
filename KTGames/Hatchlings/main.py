import arcade
import random
from MainView import MainView

""" CONSTANTS """
# screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TITLE = "Hatchlings"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    main_view = MainView()
    window.show_view(main_view)
    main_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()

