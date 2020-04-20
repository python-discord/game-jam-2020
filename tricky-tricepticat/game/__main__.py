"""
Tricky Tricepticat
Domicidal
Python Discord | Game Jam 2020
"""
# Standard Library
import os
from pathlib import Path

# Third Party
import arcade
from math import atan2, degrees
from pyglet import gl

UPDATES_PER_FRAME = 3

PLAYER_MOVEMENT_SPEED = 300
SHIP_MOVEMENT_SPEED = 200

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 100
RIGHT_VIEWPORT_MARGIN = 100
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

CHARACTER_SCALING = 1
SHIP_SCALING = 1

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
path['maps'] = path['resources'] / "maps"


def load_texture_pair(filename):
    '''
    Load a texture pair, with the second being a mirror image.
    '''
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class Ship(arcade.Sprite):
    '''
    Playable Pirate Ship
    '''
    def __init__(self, filename):
        super().__init__(filename)
        self.name = 'Ship'

        self.scale = SHIP_SCALING


class Pirate(arcade.Sprite):
    '''
    Player class
    '''
    def __init__(self, sprite_root):
        super().__init__()
        self.name = sprite_root

        self.scale = CHARACTER_SCALING

        sprite_path = path['img'] / sprite_root
        self.texture_dict = {}
        self.texture_dict['run'] = [
            load_texture_pair(sprite_path / "run" / f"{i}.png")
            for i in range(1, len(os.listdir(sprite_path / "run"))+1)
        ]
        self.texture_dict['idle'] = [
            load_texture_pair(sprite_path / "idle" / f"{i}.png")
            for i in range(1, len(os.listdir(sprite_path / "idle"))+1)
        ]
        self.texture_dict['attack'] = [
            load_texture_pair(sprite_path / "attack" / f"{i}.png")
            for i in range(1, len(os.listdir(sprite_path / "attack"))+1)
        ]

        self.texture = self.texture_dict['idle'][0][0]
        self.bottom = 0

        self.cur_run_texture = 0
        self.cur_idle_texture = 0
        self.cur_attack_texture = 0

        self.character_face_direction = RIGHT_FACING

        self.is_idle = False

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
        if self.is_idle:
            frames = self.cur_idle_texture // UPDATES_PER_FRAME

            if frames == len(self.texture_dict['idle'])-1:
                self.cur_idle_texture = 0

            print(self.name, frames)
            self.texture = self.texture_dict['idle'][frames][
                self.character_face_direction
                ]

            self.cur_idle_texture += 1
            return

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.texture_dict['idle'][0][
                self.character_face_direction
                ]
            self.cur_run_texture, self.cur_idle_texture = 0, 0
            return

        # Walking animation

        frames = self.cur_run_texture // UPDATES_PER_FRAME

        if frames == len(self.texture_dict['run'])-1:
            self.cur_run_texture = 0

        self.texture = self.texture_dict['run'][frames][
            self.character_face_direction
            ]

        self.cur_run_texture += 1

    def on_update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        # if self.left < 0:
        #     self.left = 0
        # elif self.right > SCREEN_WIDTH - 1:
        #     self.right = SCREEN_WIDTH - 1
        #
        # if self.bottom < 0:
        #     self.bottom = 0
        # elif self.top > SCREEN_HEIGHT - 1:
        #     self.top = SCREEN_HEIGHT - 1

        self.update_animation()


class ShipView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.ship_sprite = Ship(path['img']/'ship'/'ship.png')

        self.ship_sprite.set_position(800, 800)

        self.layer_shift_count = 0
        self.map = arcade.tilemap.read_tmx(path['maps'] / "test_map.tmx")

        self.map_layers = [arcade.process_layer(
            self.map, layer.name) for layer in self.map.layers]

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.ship_sprite, self.map_layers[2])

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # self.player_view = PlayerView()

        self.ship_sprite.target_angle = 0

    def scroll(self):
        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        # changed = False
        #
        # # Scroll left
        # left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        # if self.ship_sprite.left < left_boundary:
        #     self.view_left -= left_boundary - self.ship_sprite.left
        #     changed = True
        #
        # # Scroll right
        # right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        # if self.ship_sprite.right > right_boundary:
        #     self.view_left += self.ship_sprite.right - right_boundary
        #     changed = True
        #
        # # Scroll up
        # top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        # if self.ship_sprite.top > top_boundary:
        #     self.view_bottom += self.ship_sprite.top - top_boundary
        #     changed = True
        #
        # # Scroll down
        # bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        # if self.ship_sprite.bottom < bottom_boundary:
        #     self.view_bottom -= bottom_boundary - self.ship_sprite.bottom
        #     changed = True
        #
        # if changed:
        #     # Only scroll to integers. Otherwise we end up with pixels that
        #     # don't line up on the screen
        #     self.view_bottom = int(self.view_bottom)
        #     self.view_left = int(self.view_left)

            # Do the scrolling
            # arcade.set_viewport(self.view_left,
            #                     SCREEN_WIDTH + self.view_left,
            #                     self.view_bottom,
            #                     SCREEN_HEIGHT + self.view_bottom)
            left = int(self.ship_sprite._get_position()[0]-SCREEN_WIDTH/2)
            right = int(self.ship_sprite._get_position()[0]+SCREEN_WIDTH/2)
            bottom = int(self.ship_sprite._get_position()[1]-SCREEN_HEIGHT/2)
            top = int(self.ship_sprite._get_position()[1]+SCREEN_HEIGHT/2)

            if left < 75:
                left = 75
                right = 75+SCREEN_WIDTH
            if right > 4000:
                right = 4000
                left = right-SCREEN_WIDTH
            if top > 2300:
                top = 2300
                bottom = 2300 - SCREEN_HEIGHT
            if bottom < 0:
                bottom = 0
                top = SCREEN_HEIGHT

            arcade.set_viewport(left, right, bottom, top)

    def on_show(self):
        print("Switched to ShipView")
        print(self.window.get_viewport())

    def on_draw(self):
        arcade.start_render()

        for layer in self.map_layers:
            layer.draw()

        self.ship_sprite.draw()

    def on_update(self, delta_time):
        print(self.ship_sprite._get_position(), self.ship_sprite._get_angle())
        self.scroll()

        self.map_layers[0].move(1, 0)
        self.layer_shift_count += 1
        if self.layer_shift_count == 64:
            self.map_layers[0].move(-64, 0)
            self.layer_shift_count = 0

        # Calculate speed based on the keys pressed
        self.ship_sprite.change_x = 0
        self.ship_sprite.change_y = 0

        self.ship_sprite.change_angle = 0

        if self.up_pressed and not self.down_pressed:
            self.ship_sprite.change_y = SHIP_MOVEMENT_SPEED * delta_time
            if int(self.ship_sprite.angle)%360 != 180:
                self.ship_sprite.change_angle = 1
                if int(self.ship_sprite.angle)%360 not in range(0, 180):
                    self.ship_sprite.change_angle = -1
        elif self.down_pressed and not self.up_pressed:
            self.ship_sprite.change_y = -SHIP_MOVEMENT_SPEED * delta_time
            if int(self.ship_sprite.angle)%360 != 0:
                self.ship_sprite.change_angle = 1
                if int(self.ship_sprite.angle)%360 in range(0, 180):
                    self.ship_sprite.change_angle = -1
        if self.left_pressed and not self.right_pressed:
            self.ship_sprite.change_x = -SHIP_MOVEMENT_SPEED * delta_time
            if int(self.ship_sprite.angle)%360 != 270:
                self.ship_sprite.change_angle = 1
                if int(self.ship_sprite.angle)%360 not in range(90, 270):
                    self.ship_sprite.change_angle = -1
        elif self.right_pressed and not self.left_pressed:
            self.ship_sprite.change_x = SHIP_MOVEMENT_SPEED * delta_time
            if int(self.ship_sprite.angle)%360 != 90:
                self.ship_sprite.change_angle = 1
                if int(self.ship_sprite.angle)%360 in range(90, 270):
                    self.ship_sprite.change_angle = -1

        # self.ship_sprite.on_update(delta_time)

        # print(self.get_viewport())
        width, height = arcade.get_viewport()[1], arcade.get_viewport()[3]

        if self.ship_sprite.left < 0:
            self.ship_sprite.left = 0
        elif self.ship_sprite.right > width - 1:
            self.ship_sprite.right = width - 1

        if self.ship_sprite.bottom < 0:
            self.ship_sprite.bottom = 0
        elif self.ship_sprite.top > height - 1:
            self.ship_sprite.top = height - 1

        self.physics_engine.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False


class PlayerView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.player_sprites = arcade.SpriteList()

        self.player_sprite = Pirate('captain')

        for i in ('brawn', 'bald'):
            self.player_sprites.append(Pirate(i))
        self.player_sprites[0].center_x = 400
        self.player_sprites[1].center_x = 600
        self.player_sprite.center_x = 800

        self.map = arcade.tilemap.read_tmx(path['maps'] / "test_map.tmx")

        self.map_layers = [arcade.process_layer(
            self.map, layer.name) for layer in self.map.layers]

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.map_layers[2])

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def scroll(self):
        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_show(self):
        print("Switched to PlayerView")

    def on_draw(self):
        arcade.start_render()
        self.player_sprite.draw()
        self.player_sprites.draw(filter=gl.GL_NEAREST)

    def on_update(self, delta_time):

        self.scroll()

        self.player_sprite.update_animation()

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED * delta_time
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED * delta_time
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED * delta_time
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED * delta_time

        # print(self.get_viewport())
        width, height = arcade.get_viewport()[1:4:2]

        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > width - 1:
            self.player_sprite.right = width - 1

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > height - 1:
            self.player_sprite.top = height - 1

        self.physics_engine.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)


        # If you have sprite lists, you should create them here,
        # and set them to None


    def setup(self):
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame
        arcade.start_render()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass
        # self.scroll()

        # Call update to move the sprite
        # If using a physics engine, call update on it instead of the sprite
        # list.
        # self.player_sprites.on_update(delta_time)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

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
    # window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    ship_view = ShipView()
    player_view = PlayerView()

    window.show_view(ship_view)

    arcade.run()


if __name__ == "__main__":
    main()
