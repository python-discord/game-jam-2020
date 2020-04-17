import arcade

# Constants
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960
WINDOW_TITLE = 'MyPythonGame'

TILE_SIZE = 32#x32

# Scaling constants
PLAYER_SCALING = 1
TILE_SCALING = 1

# Class defining
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, windowTitle):
        super(MyGame, self).__init__(width, height, windowTitle, resizable=False)

        self.tile_list = None
        self.player_list = None

        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()

        for x in range(0, WINDOW_WIDTH, 32):
            for y in range(0, WINDOW_HEIGHT, 32):
                wall = arcade.Sprite(r"images\tiles\grassTile.png", TILE_SCALING)
                wall.center_x = x + TILE_SIZE/2
                wall.center_y = y + TILE_SIZE/2
                self.tile_list.append(wall)

    def on_draw(self):
        """ Renders the screen. """

        arcade.start_render()
        self.tile_list.draw()

    def on_update(self, delta_time: float):
        """ On Update method"""
        pass



    def on_key_press(self, symbol: int, modifiers: int):
        """ Get keyboard's presses. """
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        """ Get keyboard's releases. """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse's presses. """
        pass

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Get mouse's releases. """
        pass

# MAIN
def main():
    """ Main method """
    window = MyGame(WINDOW_WIDTH,WINDOW_HEIGHT,WINDOW_TITLE)
    print('Window created')
    window.setup()
    print('Game set up')
    arcade.run()

if __name__ == "__main__":
    main()

else:
    print('wtf you do')