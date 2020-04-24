import arcade
from main import *


class Main:

    def __init__(self):
        self.settings = Settings(self)
        self.menu = MainMenu(self)
        self.window = arcade.Window(self.menu.width, self.menu.height, "MENU")


if __name__ == "__main__":
    main = Main()
    main.window.show_view(main.menu)
    arcade.run()
