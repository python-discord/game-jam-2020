# setup
import arcade
# from arcade.gui import *
from submission.gameConstants import *
from submission.loadAnimatedChars import *
from submission.tileMapLoader import *
from submission.sounds import loadSounds
from random import randint
import math

def getGridCase(position):
    case = [math.floor(position[0]/32)-22*FULLSCREEN,math.floor(position[1]/32)-9*FULLSCREEN]
    print(case)
    return case

# Class defining
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, windowTitle):
        if FULLSCREEN:
            super(MyGame, self).__init__(width, height, windowTitle, fullscreen=True)
        else:
            super(MyGame, self).__init__(width, height, windowTitle, fullscreen=False)

        self.ground_list = None
        self.path_list = None
        self.player_list = None
        self.entity_list = None

        self.player_sprite = None

        self.game_mode = ''

        self.mouse_x = 0
        self.mouse_y = 0

        self.mouse_click = [0,0]
        self.destination = [0,0]

        self.sound_dict = {}

        self.window_offset_x = 0
        self.window_offset_y = 0

        self.screen_x = 0
        self.screen_y = 0

        self.mosquito = None

        arcade.set_background_color((94, 132, 63))

    def setup(self):
        """ Set up the test here. Call this function to restart the test. """
        if FULLSCREEN:
            self.screen_x, self.screen_y = self.get_size()
            self.window_offset_x = self.screen_x/2 - WINDOW_WIDTH/2
            self.window_offset_y = self.screen_y/2 - WINDOW_HEIGHT/2

        self.player_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.path_list = arcade.SpriteList()
        self.entity_list = arcade.SpriteList()

        self.player_sprite = AnimatedPlayer('player', 4)
        self.player_list.append(self.player_sprite)

        self.path_list = loadPathTilemap()

        for i in range(len(self.path_list)):
            self.path_list[i].center_x += self.window_offset_x
            self.path_list[i].center_y += self.window_offset_y

        for x in range(0, WINDOW_WIDTH, TILE_SIZE):  # Crée le fond à l'aide des grasstiles
            for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
                randomNum = randint(1,3)
                ground = arcade.Sprite(PATH['img'] / f"tiles\\grassTile{randomNum}.png", TILE_SCALING)
                ground.center_x = x + TILE_SIZE * TILE_SCALING / 2 + self.window_offset_x
                ground.center_y = y + TILE_SIZE * TILE_SCALING / 2 + self.window_offset_y
                self.ground_list.append(ground)

        loadSounds(PATH['sound'], self.sound_dict)


    def on_draw(self):
        """ Renders the screen. """

        arcade.start_render()
        # Ground layer
        self.ground_list.draw()
        self.path_list.draw()
        # Entity layer
        self.entity_list.draw()
        # Turetts layer

        # Player layer
        self.player_sprite.draw()

        # GUI layer

    def on_update(self, delta_time: float):
        """ On Update method"""
        if self.destination != [-1,-1]:
            self.player_sprite.center_x = self.destination[0] * TILE_SIZE + TILE_SIZE/2 + self.window_offset_x
            self.player_sprite.center_y = self.destination[1] * TILE_SIZE + TILE_SIZE/2 + self.window_offset_y
            self.destination = [-1,-1]

        self.player_list.update_animation()
        self.entity_list.update_animation()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Get keyboard's presses. """
        self.mosquito = AnimatedEntity('fourmi', 4, E_MOSQUITO)
        self.mosquito.center_x = self.screen_x/2
        self.mosquito.center_y = self.screen_y/2
        self.entity_list.append(self.mosquito)

    def on_key_release(self, symbol: int, modifiers: int):
        """ Get keyboard's releases. """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """ Get mouse's presses. """
        if FULLSCREEN:
            if self.mouse_x > self.screen_x/2 + WINDOW_WIDTH/2 or self.mouse_x < self.screen_x/2 - WINDOW_WIDTH/2:
                print('Cannot move')
            elif self.mouse_y > self.screen_y/2 + WINDOW_HEIGHT/2 or self.mouse_y < self.screen_y/2 - WINDOW_HEIGHT/2:
                print('Cannot move')

            else:
                self.mouse_click = [self.mouse_x, self.mouse_y]
                self.destination = getGridCase(self.mouse_click)
                if button == 1:  # Si clique gauche
                    pass
                elif button == 4:  # Si clique droit
                    pass
        else:
            self.mouse_click = [self.mouse_x, self.mouse_y]
            self.destination = getGridCase(self.mouse_click)
            if button == 1: # Si clique gauche
                pass
            elif button == 4: # Si clique droit
                pass


    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Get mouse's releases. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_x = x
        self.mouse_y = y