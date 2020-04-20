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
from pyglet import gl

UPDATES_PER_FRAME = 3

MOVEMENT_SPEED = 300

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 100
RIGHT_VIEWPORT_MARGIN = 100
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

SPRITE_SCALING = 0.5

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


class Pirate(arcade.Sprite):
    '''
    Player class
    '''
    def __init__(self, sprite_root):
        super().__init__()
        self.name = sprite_root

        self.scale = SPRITE_SCALING

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


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        arcade.set_background_color(arcade.color.AMAZON)

        self.player_sprites = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # If you have sprite lists, you should create them here,
        # and set them to None

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

    def setup(self):
        # Create your sprites and sprite lists here
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

        self.layer_positions = [layer._get_position() for layer in self.map_layers[0]]

        self.layer_shift_count = 0

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.map_layers[2])

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame
        arcade.start_render()

        for layer in self.map_layers:
            layer.draw()

        self.player_sprite.draw()
        self.player_sprites.draw(filter=gl.GL_NEAREST)

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.scroll()

        self.player_sprite.update_animation()

        self.map_layers[0].move(1,0)
        self.layer_shift_count += 1
        if self.layer_shift_count == 64:
            self.map_layers[0].move(-64, 0)
            self.layer_shift_count = 0


        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED * delta_time
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED * delta_time
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED * delta_time
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED * delta_time

        # print(self.get_viewport())
        width, height = self.get_viewport()[1:4:2]

        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > width - 1:
            self.player_sprite.right = width - 1

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > height - 1:
            self.player_sprite.top = height - 1

        self.physics_engine.update()

        # for sprite in self.player_sprites:
        #     # Calculate speed based on the keys pressed
        #     sprite.change_x = 0
        #     sprite.change_y = 0
        #
        #     if self.up_pressed and not self.down_pressed:
        #         sprite.change_y = MOVEMENT_SPEED * delta_time
        #     elif self.down_pressed and not self.up_pressed:
        #         sprite.change_y = -MOVEMENT_SPEED * delta_time
        #     if self.left_pressed and not self.right_pressed:
        #         sprite.change_x = -MOVEMENT_SPEED * delta_time
        #     elif self.right_pressed and not self.left_pressed:
        #         sprite.change_x = MOVEMENT_SPEED * delta_time
        #
        #     # print(self.get_viewport())
        #     width, height = self.get_viewport()[1:4:2]
        #
        #     if sprite.left < 0:
        #         sprite.left = 0
        #     elif sprite.right > width - 1:
        #         sprite.right = width - 1
        #
        #     if sprite.bottom < 0:
        #         sprite.bottom = 0
        #     elif sprite.top > height - 1:
        #         sprite.top = height - 1

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
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
