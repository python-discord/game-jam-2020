"""
Tricky Tricepticat
Domicidal
Python Discord | Game Jam 2020
"""
import os
from pathlib import Path

import arcade


UPDATES_PER_FRAME = 3

MOVEMENT_SPEED = 300

SPRITE_SCALING = 3

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Game Jam 2020"

# File paths for project and resources
path = {}
path['project'] = Path(os.path.dirname(__file__))
path['resources'] = path['project'] / "resources"
path['img'] = path['resources'] / "img"
path['sound'] = path['resources'] / "sound"


def load_texture_pair(filename):
    '''
    Load a texture pair, with the second being a mirror image.
    '''
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class Pirate(arcade.Sprite):
    '''
    Player class
    '''
    def __init__(self, sprite_root):
        super().__init__()
        sprite_path = path['img'] / sprite_root
        self.texture_dict = {}
        self.texture_dict['run'] = [
            load_texture_pair(sprite_path / "run" / i)
            for i in os.listdir(sprite_path / "run")
        ]
        self.texture_dict['idle'] = [
            load_texture_pair(sprite_path / "idle" / i)
            for i in os.listdir(sprite_path / "idle")
        ]
        self.texture_dict['attack'] = [
            load_texture_pair(sprite_path / "attack" / i)
            for i in os.listdir(sprite_path / "attack")
        ]

        self.texture = self.texture_dict['idle'][0][0]
        self.bottom = 0

        self.cur_texture = 0

        self.character_face_direction = RIGHT_FACING

    def update_animation(self):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING

        elif (
                self.change_x > 0 and
                self.character_face_direction == LEFT_FACING
             ):
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture > len(
                    self.texture_dict['idle']
                    ) + 1 * UPDATES_PER_FRAME:
                self.cur_texture = len(self.texture_dict['idle'])
                self.cur_texture -= 1
            frames = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.texture_dict['idle'][frames][
                self.character_face_direction
                ]
            self.texture = self.texture_dict['idle'][0][
                self.character_face_direction
                ]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > len(
                self.texture_dict['run'])+1 * UPDATES_PER_FRAME:
            self.cur_texture = 0

        frames = self.cur_texture // UPDATES_PER_FRAME

        self.texture = self.texture_dict['run'][frames][
            self.character_face_direction
            ]

    def on_update(self, delta_time):
        self.center_x += self.change_x*MOVEMENT_SPEED*delta_time
        self.center_y += self.change_y*MOVEMENT_SPEED*delta_time


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)

        self.player_sprite = None

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here
        self.player_sprite = Pirate('brawn')
        self.player_sprite.center_x = 400

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame
        arcade.start_render()

        self.player_sprite.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_sprite.change_x = 0.1
        self.player_sprite.change_y = 0
        self.player_sprite.on_update(delta_time)
        self.player_sprite.update_animation()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
