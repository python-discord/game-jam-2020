# setup
import arcade
from arcade.gui import *
from gameConstants import *


def getGridCase(position):
    pass

def createGrid():
    size = int(WINDOW_WIDTH / 32)


# Class defining
"""class PlayButton(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text=TextButton, theme=None):
        super().__init__(x,y,width,height,text,theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True
        print('FUCK YEAH')"""

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, windowTitle):
        super(MyGame, self).__init__(width, height, windowTitle, resizable=False)

        self.tile_list = None
        self.player_list = None

        self.player_sprite = None

        self.game_mode = ''

        self.mouse_x = 0
        self.mouse_y = 0

        self.destination = [0,0]

        createGrid()

        arcade.set_background_color(arcade.csscolor.PURPLE)

        """self.pause = False
        self.speed = 1
        self.theme = None

    def set_button_textures(self):
        normal = PATH_ADD + "images\\tiles\\button.png"
        hover = PATH_ADD + "images\\tiles\\button.png"
        clicked = PATH_ADD + "images\\tiles\\button.png"
        locked = PATH_ADD + "images\\tiles\\button.png"

        self.theme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE)
        self.set_button_textures()

    def set_buttons(self):
        self.button_list.append(PlayButton(self, 60, 570, 110, 50, theme=self.theme))"""

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player_list = arcade.SpriteList()
        self.tile_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(PATH_ADD + "images\\sprite\\player.png", PLAYER_SCALING)
        self.player_sprite.center_x = WINDOW_WIDTH/2
        self.player_sprite.center_y = WINDOW_HEIGHT/2
        self.player_list.append(self.player_sprite)

        for x in range(0, WINDOW_WIDTH, TILE_SIZE):  # Crée le fond à l'aide de grassTile.png
            for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
                wall = arcade.Sprite(PATH_ADD+"images\\tiles\\grassTile.png", TILE_SCALING)
                wall.center_x = x + TILE_SIZE / 2
                wall.center_y = y + TILE_SIZE / 2
                self.tile_list.append(wall)

        """self.setup_theme()
        self.set_buttons()"""

    def on_draw(self):
        """ Renders the screen. """

        arcade.start_render()
        # Ground layer
        self.tile_list.draw()
        arcade.draw_point(self.destination[0], self.destination[1], arcade.csscolor.WHITE, 5)
        # Player layer
        self.player_sprite.draw()

        # GUI layer
        """"self.button_list.draw()"""

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
        self.destination = [self.mouse_x, self.mouse_y]
        print(self.destination)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Get mouse's releases. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y