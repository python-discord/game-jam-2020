"""
Tricky Tricepticat
Domicidal
Python Discord | Game Jam 2020
"""
# Standard Library
import os
from pathlib import Path
import time

# Third Party
import arcade
from math import atan2, degrees, radians, sin, cos, sqrt
from pyglet import gl

UPDATES_PER_FRAME = 3

PLAYER_MOVEMENT_SPEED = 300
SHIP_MOVEMENT_SPEED = 200
CANNONBALL_SPEED = 50

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

CHARACTER_SCALING = 0.5
SHIP_SCALING = 1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

MUSIC_VOLUME = 0.2

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

        self.health = 100

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
        self.is_attacking = False
        self.follower = False

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

        # Attack animation
        elif self.is_attacking:
            frames = self.cur_attack_texture // UPDATES_PER_FRAME

            if frames == len(self.texture_dict['attack'])-1:
                self.cur_attack_texture = 0
                self.is_attacking = False
                return

            self.texture = self.texture_dict['attack'][frames][
                self.character_face_direction
                ]

            self.cur_attack_texture += 1

        # Default animation
        elif self.change_x == 0 and self.change_y == 0:
            self.texture = self.texture_dict['idle'][0][
                self.character_face_direction
                ]
            (self.cur_run_texture, self.cur_idle_texture,
                self.cur_attack_texture) = (0, 0, 0)
            return

        # Walking animation
        else:
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

        for i in (50, 25, 0):
            self.ship_sprite.append_texture(
                arcade.load_texture(path['img'] / 'ship' / f'ship_{i}.png'))

        self.cannonballs = arcade.SpriteList()

        self.ship_sprite.set_position(800, 800)

        self.layer_shift_count = 0
        self.seafoam_shift_count = 64
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

        self.SAIL_SPEED_FACTOR = 0

        self.audio_list = []
        self.music = arcade.Sound(
            str(path['sound'] / "shanty1.mp3"), streaming=True
        )

        self.ambient_track = arcade.Sound(
            str(path['sound'] / "ship_ambient.mp3"), streaming=True
        )



        self.audio_list.append(self.music)
        self.audio_list.append(self.ambient_track)

        for audio in self.audio_list:
            audio.play()

        self.music.set_volume(MUSIC_VOLUME*0.2)
        self.ambient_track.set_volume(MUSIC_VOLUME*0.2)

        self.viewport_scale = 1

        self.collision_time = 0
        self.time_diff = 20

    def scroll(self):
        # --- Manage Scrolling ---

        if self.viewport_scale < 0.5:
            self.viewport_scale = 0.5

        if self.viewport_scale > 3.0:
            self.viewport_scale = 3.0

        left = int(
            self.ship_sprite._get_position()[0] -
            SCREEN_WIDTH / 2 * self.viewport_scale)
        right = int(
            self.ship_sprite._get_position()[0] +
            SCREEN_WIDTH / 2 * self.viewport_scale)
        bottom = int(
            self.ship_sprite._get_position()[1] -
            SCREEN_HEIGHT / 2 * self.viewport_scale)
        top = int(
            self.ship_sprite._get_position()[1] +
            SCREEN_HEIGHT / 2 * self.viewport_scale)

        if left < 75:
            left = 75
            right = 75+SCREEN_WIDTH*self.viewport_scale
        if right > 4000:
            right = 4000
            left = right-SCREEN_WIDTH*self.viewport_scale
        if top > 2300:
            top = 2300
            bottom = 2300 - SCREEN_HEIGHT*self.viewport_scale
        if bottom < 0:
            bottom = 0
            top = SCREEN_HEIGHT*self.viewport_scale

        if True:
            arcade.set_viewport(
                int(left),
                int(right),
                int(bottom),
                int(top)
            )

    def on_show(self):
        print("Switched to ShipView")
        # print(self.window.get_viewport())

    def play_audio(self):
        for audio in self.audio_list:
            if audio.get_stream_position() >= audio.get_length():
                file_name = audio.file_name
                volume = audio.get_volume()
                self.audio_list.remove(audio)
                newAudio = arcade.Sound(
                    file_name, streaming=True
                )

                self.audio_list.append(newAudio)

                audio.play(newAudio.get_volume())

    def on_draw(self):
        arcade.start_render()

        for layer in self.map_layers:
            layer.draw(filter=gl.GL_NEAREST)

        self.cannonballs.draw()

        self.ship_sprite.draw()

    def on_update(self, delta_time):

        self.cannonballs.update()

        self.scroll()

        self.map_layers[0].move(1, 0)
        if self.seafoam_shift_count > 0:
            self.map_layers[1].move(0.25, 0.25)
            self.seafoam_shift_count -= 0.25

        self.layer_shift_count += 1
        if self.layer_shift_count == 64:
            self.map_layers[0].move(-64, 0)
            # self.map_layers[1].move(-16, 0)
            self.layer_shift_count = 0

        if self.seafoam_shift_count <= 0:
            self.map_layers[1].move(-0.25, -0.25)
            self.seafoam_shift_count -= 0.25
        if self.seafoam_shift_count == -64:
            self.seafoam_shift_count = 64


        # Calculate speed based on the keys pressed
        # self.ship_sprite.change_x = 0
        # self.ship_sprite.change_y = 0

        if self.SAIL_SPEED_FACTOR < 0:
            self.SAIL_SPEED_FACTOR = 0

        if self.SAIL_SPEED_FACTOR > 1:
            self.SAIL_SPEED_FACTOR = 1

        self.ship_sprite.change_y = (
            self.SAIL_SPEED_FACTOR * SHIP_MOVEMENT_SPEED * sin(radians(
                self.ship_sprite.angle % 360 - 90)
            ) * delta_time
        )

        self.ship_sprite.change_x = (
            self.SAIL_SPEED_FACTOR * SHIP_MOVEMENT_SPEED * cos(radians(
                self.ship_sprite.angle % 360 - 90)
            ) * delta_time
        )


        self.ship_sprite.change_angle = 0

        if self.up_pressed and not self.down_pressed:
            self.SAIL_SPEED_FACTOR += 0.01

        elif self.down_pressed and not self.up_pressed:
            self.SAIL_SPEED_FACTOR -= 0.005

        if self.left_pressed and not self.right_pressed:
            self.ship_sprite.change_angle = 1

        elif self.right_pressed and not self.left_pressed:
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

        collided_walls = self.physics_engine.update()
        wall_collision = len(collided_walls) > 0

        # print(f"{self.ship_sprite.health, collided_walls}")
        speed = sqrt(self.ship_sprite.change_x**2 + self.ship_sprite.change_y**2)

        if wall_collision:
            self.collision_time = time.time()
        else:
            self.time_diff = time.time() - self.collision_time

        print((time.time(), self.collision_time, self.time_diff))

        if wall_collision and speed > 0.1 and self.time_diff > 2:
            self.ship_sprite.health -= 20

        if int(self.ship_sprite.health) in range(25, 51):
            self.ship_sprite.set_texture(1)
            self.ship_sprite.change_y *= 0.5
            self.ship_sprite.change_x *= 0.5

        elif int(self.ship_sprite.health) in range(1, 25):
            self.ship_sprite.set_texture(2)
            self.ship_sprite.change_y *= 0.25
            self.ship_sprite.change_x *= 0.25

        self.time_diff = time.time() - self.collision_time

        # Death condition
        if int(self.ship_sprite.health) <= 0:
            self.ship_sprite.set_texture(3)
            self.SAIL_SPEED_FACTOR = 0

        self.play_audio()

        # print((self.time_diff, speed, wall_collision, wall_collision and speed > 1 and self.time_diff > 2))

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
        if key == arcade.key.Q:
            cannonball = arcade.Sprite(path['img'] / 'ship' / 'cannonBall.png', 1)

            start_x, start_y = self.ship_sprite._get_position()
            cannonball.set_position(start_x, start_y)

            cannonball.change_x = cos(radians(self.ship_sprite.angle)) * CANNONBALL_SPEED
            cannonball.change_y = sin(radians(self.ship_sprite.angle)) * CANNONBALL_SPEED

            print(self.ship_sprite.angle%360)

            self.cannonballs.append(cannonball)

            # TODO: Add collision detection to remove sprites and cause damage

        if key == arcade.key.E:
            cannonball = arcade.Sprite(path['img'] / 'ship' / 'cannonBall.png', 1)

            start_x, start_y = self.ship_sprite._get_position()
            cannonball.set_position(start_x, start_y)

            cannonball.change_x = cos(radians(self.ship_sprite.angle+180)) * CANNONBALL_SPEED
            cannonball.change_y = sin(radians(self.ship_sprite.angle+180)) * CANNONBALL_SPEED

            print(self.ship_sprite.angle%360)

            self.cannonballs.append(cannonball)

        if key == arcade.key.EQUAL:
            self.viewport_scale -= 0.5
        if key == arcade.key.MINUS:
            self.viewport_scale += 0.5

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
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 200

        self.player_sprites.append(self.player_sprite)

        self.map = arcade.tilemap.read_tmx(path['maps'] / "dungeon_test.tmx")

        self.map_layers = [arcade.process_layer(
            self.map, layer.name) for layer in self.map.layers]

        self.physics_engines = []

        for sprite in self.player_sprites:
            self.physics_engines.append(
                arcade.PhysicsEngineSimple(
                    sprite, self.map_layers[2]
                )
            )

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def scroll(self):
        self.viewport_scale = 0.5
        # position_changed = (
        #     self.up_pressed or
        #     self.down_pressed or
        #     self.left_pressed or
        #     self.right_pressed
        # )

        left = int(self.player_sprite._get_position()[0]-SCREEN_WIDTH/2*self.viewport_scale)
        right = int(self.player_sprite._get_position()[0]+SCREEN_WIDTH/2*self.viewport_scale)
        bottom = int(self.player_sprite._get_position()[1]-SCREEN_HEIGHT/2*self.viewport_scale)
        top = int(self.player_sprite._get_position()[1]+SCREEN_HEIGHT/2*self.viewport_scale)

        if left < 0:
            left = 0
            right = 0+SCREEN_WIDTH*self.viewport_scale
        if right > 4000:
            right = 4000
            left = right-SCREEN_WIDTH*self.viewport_scale
        if top > 2300:
            top = 2300
            bottom = 2300 - SCREEN_HEIGHT*self.viewport_scale
        if bottom < 0:
            bottom = 0
            top = SCREEN_HEIGHT*self.viewport_scale

        if True:
            arcade.set_viewport(
                left,
                right,
                bottom,
                top
            )

    def on_show(self):
        print("Switched to PlayerView")

    def on_draw(self):
        arcade.start_render()
        for layer in self.map_layers:
            layer.draw(filter=gl.GL_NEAREST)
        # self.player_sprite.draw()
        self.player_sprites.draw(filter=gl.GL_NEAREST)

    def on_update(self, delta_time):

        self.scroll()

        for sprite in self.player_sprites:
            sprite.update_animation()

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

        count = 0
        for sprite in self.player_sprites:
            count += 1
            if sprite is not self.player_sprite:
                if self.player_sprite.is_attacking:
                    sprite.is_attacking = True
                sprite.character_face_direction = self.player_sprite.character_face_direction
                sprite.change_x, sprite.change_y = self.player_sprite.change_x, self.player_sprite.change_y
                if sprite.collides_with_list(self.map_layers[2]):
                    print(f"{self.player_sprites.index(sprite)}. YEP.")
                if count == 1:
                    sprite.set_position(self.player_sprite.center_x, self.player_sprite.center_y+30*count)
                else:
                    sprite.set_position(self.player_sprite.center_x, self.player_sprite.center_y-15*count)
                # if self.player_sprite.character_face_direction == RIGHT_FACING:
                #     sprite.set_position(self.player_sprite.center_x, self.player_sprite.center_y-30*count)
                # else:
                    # sprite.set_position(self.player_sprite.center_x, self.player_sprite.center_y+30*count)

        for engine in self.physics_engines:
            engine.update()

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

        if key == arcade.key.E:
            self.player_sprite.is_attacking = True
            print(self.player_sprite.is_attacking)

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
    # window.show_view(player_view)

    arcade.run()


if __name__ == "__main__":
    main()
