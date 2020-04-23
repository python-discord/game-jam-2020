"""
Tricky Tricepticat
Domicidal
Python Discord | Game Jam 2020
"""
# Standard Library
from math import atan2, degrees, radians, sin, cos, sqrt
import os
from pathlib import Path
import pprint
import random
import time

# Third Party
import arcade
import PIL
from pyglet import gl

UPDATES_PER_FRAME = 3

PLAYER_MOVEMENT_SPEED = 150
SHIP_MOVEMENT_SPEED = 200
CANNONBALL_SPEED = 20

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


class Weapon(arcade.Sprite):
    def __init__(self, sprite_root):
        super().__init__()
        sprite_path = path['img'] / sprite_root

        self.scale = 1

        self.texture_dict = {}

        for i in os.listdir(sprite_path):
            self.texture_dict[i] = []
            for j in range(1, len(os.listdir(sprite_path / i))+1):
                self.texture_dict[i].append(load_texture_pair(
                    sprite_path / i / f"({j}).png"))

        self.texture = self.texture_dict['sword_stab'][0][0]

        self.is_stab = False
        self.is_cut = False

        self.cur_stab_texture = 0
        self.cur_cut_texture = 0

        # print(self.texture_dict)

    def update_animation(self):

        # Attack animation
        if self.is_stab:
            frames = self.cur_stab_texture // UPDATES_PER_FRAME

            if frames == len(self.texture_dict['sword_stab'])-1:
                self.cur_stab_texture = 0
                self.is_stab = False
                return

            self.texture = self.texture_dict['sword_stab'][frames][0]

            self.cur_stab_texture += 1

        if self.is_cut:
            frames = self.cur_cut_texture // UPDATES_PER_FRAME

            if frames == len(self.texture_dict['sword_cut'])-1:
                self.cur_cut_texture = 0
                self.is_cut = False
                self.texture = self.texture_dict['sword_stab'][0][0]
                return

            self.texture = self.texture_dict['sword_cut'][frames][0]

            self.cur_cut_texture += 1


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


class Enemy_SpriteSheet(arcade.Sprite):
    def __init__(self, sprite_root):
        super().__init__()
        self.character_face_direction = LEFT_FACING

        self.health = 100

        self.is_idle = False
        self.is_hit = False
        self.is_attacking = False

        self.cur_idle_texture = 0
        self.cur_attack_texture = 0
        self.cur_run_texture = 0
        self.cur_hit_texture = 0

        self.right_facing_textures = [
            arcade.load_spritesheet(
                path['img'] / sprite_root / f'{i}.png', PIL.Image.open(path['img'] / sprite_root / f'{i}.png').size[0]/j, PIL.Image.open(path['img'] / sprite_root / f'{i}.png').size[1], j, j)
            for (i, j) in zip(
                ('attack', 'death', 'hurt', 'idle', 'walk'),
                (20, 13, 16, 18, 20))
        ]

        self.left_facing_textures = []

        for animation in self.right_facing_textures:
            textures_list = []
            for texture in animation:
                textures_list.append(
                arcade.Texture(
                    f'{texture.name}_mirrored',
                    PIL.ImageOps.mirror(texture.image)
                ))
            self.left_facing_textures.append(textures_list)


        self.texture_dict = {}

        for (i, j) in zip(
                ('attack', 'death', 'hurt', 'idle', 'walk'),
                (0, 1, 2, 3, 4)
        ):
            self.texture_dict[i] = [
                self.right_facing_textures[j], self.left_facing_textures[j]
            ]
        # print("RIGHT", self.right_facing_textures)
        # print("LEFT", self.left_facing_textures)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.texture_dict)
        # print("DICT", self.texture_dict)
        # [[j for i in ('attack', 'death', 'hurt', 'idle', 'walk') for j in self.right_facing_textures],
        # [j for i in ('attack', 'death', 'hurt', 'idle', 'walk') for j in self.left_facing_textures]]

        self.texture = self.left_facing_textures[0][0]

    def on_update(self, delta_time):
        self.update_animation(delta_time)

        if self.health <= 0:
            self.kill()

    def update_animation(self, delta_time):
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

            if frames == len(self.texture_dict['idle'][0])-1:
                self.cur_idle_texture = 0

            # print(self.name, frames)
            self.texture = self.texture_dict['idle'][
                self.character_face_direction
                ][frames]

            self.cur_idle_texture += 1
            return

        elif self.is_hit:
            print("OW! You hit me!")
            frames = self.cur_hit_texture // UPDATES_PER_FRAME
            print(frames)

            if frames == len(self.texture_dict['hurt'][0])-1:
                self.cur_hit_texture = 0
                self.is_hit = False
                return

            self.texture = self.texture_dict['hurt'][
                self.character_face_direction
                ][frames]

            self.cur_hit_texture += 1

        # Attack animation
        elif self.is_attacking:
            frames = self.cur_attack_texture // UPDATES_PER_FRAME

            if frames == len(self.texture_dict['attack'][0])-1:
                self.cur_attack_texture = 0
                self.is_attacking = False
                return

            self.texture = self.texture_dict['attack'][
                self.character_face_direction
                ][frames]

            self.cur_attack_texture += 1

        # Default animation
        elif self.change_x == 0 and self.change_y == 0:
            self.texture = self.texture = self.texture_dict['idle'][self.character_face_direction][0]
            (self.cur_run_texture, self.cur_idle_texture,
                self.cur_attack_texture) = (0, 0, 0)
            return

        # Walking animation
        else:
            frames = self.cur_run_texture // UPDATES_PER_FRAME

            if frames == len(self.texture_dict['walk'][0])-1:
                self.cur_run_texture = 0

            self.texture = self.texture_dict['walk'][
                self.character_face_direction
                ][frames]

            self.cur_run_texture += 1


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
            str(path['sound'] / "shanty1.mp3")
        )

        self.ambient_track = arcade.Sound(
            str(path['sound'] / "ship_ambient.mp3")
        )

        self.audio_list.append(self.music)
        self.audio_list.append(self.ambient_track)

        for audio in self.audio_list:
            audio.play()

        self.music.set_volume(MUSIC_VOLUME*0.2)
        self.ambient_track.set_volume(MUSIC_VOLUME*0.4)

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
            # Have to stop and play before audio ends or the audio
            # cannot be played again
            if audio.get_stream_position() >= audio.get_length()-0.5:
                volume = audio.get_volume()
                audio.stop()
                audio.play(volume=volume)

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

        '''
        Handle wall collision damage
        '''
        collided_walls = self.physics_engine.update()
        wall_collision = len(collided_walls) > 0

        # print(f"{self.ship_sprite.health, collided_walls}")
        speed = sqrt(self.ship_sprite.change_x**2 + self.ship_sprite.change_y**2)

        if wall_collision:
            self.collision_time = time.time()
        else:
            self.time_diff = time.time() - self.collision_time

        print((time.time(), self.collision_time, self.time_diff))

        if wall_collision and speed > 0.1 and self.time_diff > 0.5:
            self.ship_sprite.health -= 10

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

        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.window.set_vsync(not self.window.vsync)

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

        self.formation = 0

        self.mouse_position = (0,0)

        arcade.set_background_color(arcade.color.AMAZON)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.player_sprites = arcade.SpriteList()

        self.player_sprite = Pirate('captain')

        # for i in ('brawn', 'bald'):
        #     self.player_sprites.append(Pirate(i))
        self.player_sprites.append(Pirate('brawn'))
        self.player_sprites.append(self.player_sprite)
        self.player_sprites.append(Pirate('bald'))

        self.player_sprites[0].set_position(200, 200)
        self.player_sprites[2].set_position(200, 200)
        self.player_sprite.set_position(200, 200)

        self.enemy_list = arcade.SpriteList()

        for i in range(5):
            self.enemy_list.append(
                Enemy_SpriteSheet('undead'))
            self.enemy_list[i].scale = 1.25
            self.enemy_list[i].set_position(random.randint(0, 500), random.randint(0, 500))

        # self.enemy_list[0].set_position(800, 200)
        # self.enemy_list[0].scale = 1.25

        self.map = arcade.tilemap.read_tmx(path['maps'] / "dungeon_test.tmx")

        self.map_layers = [arcade.process_layer(
            self.map, layer.name) for layer in self.map.layers]

        self.physics_engines = []

        for sprite in self.player_sprites:
            if sprite is self.player_sprite:
                self.physics_engines.append(
                    arcade.PhysicsEngineSimple(
                        sprite, self.map_layers[2]
                    )
                )

        # for sprite in self.enemy_list:
        #     self.physics_engines.append(
        #         arcade.PhysicsEngineSimple(
        #             sprite, self.map_layers[2]
        #         )
        #     )

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.viewport_scale = 1

        self.level_sprites = arcade.SpriteList()
        self.player_sprite.weapon = Weapon('sword')
        self.player_sprite.weapon.center_x = self.player_sprite.center_x-10
        self.player_sprite.weapon.center_x = self.player_sprite.center_y

        self.level_sprites.append(self.player_sprite.weapon)

    def scroll(self):
        # --- Manage Scrolling ---

        if self.viewport_scale < 0.25:
            self.viewport_scale = 0.25

        if self.viewport_scale > 2.0:
            self.viewport_scale = 2.0

        left = int(
            self.player_sprite._get_position()[0] -
            SCREEN_WIDTH / 2 * self.viewport_scale)
        right = int(
            self.player_sprite._get_position()[0] +
            SCREEN_WIDTH / 2 * self.viewport_scale)
        bottom = int(
            self.player_sprite._get_position()[1] -
            SCREEN_HEIGHT / 2 * self.viewport_scale)
        top = int(
            self.player_sprite._get_position()[1] +
            SCREEN_HEIGHT / 2 * self.viewport_scale)

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
        self.window.set_mouse_visible(False)

    def on_draw(self):
        arcade.start_render()
        for layer in self.map_layers:
            layer.draw(filter=gl.GL_NEAREST)
        # self.player_sprite.draw()

        self.enemy_list.draw(filter=gl.GL_NEAREST)
        self.player_sprites.draw(filter=gl.GL_NEAREST)

        self.level_sprites.draw(filter=gl.GL_NEAREST)

        # arcade.draw_line(self.mouse_position[0]*self.viewport_scale, self.mouse_position[1]*self.viewport_scale, self.player_sprite.center_x, self.player_sprite.center_y, arcade.color.RED, 1)

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
            if sprite is not self.player_sprite:
                count += 1
                if self.player_sprite.is_attacking:
                    sprite.is_attacking = True
                # sprite.character_face_direction = self.player_sprite.character_face_direction
                # direction = atan2(self.player_sprite.center_y, self.player_sprite.center_x)
                # sprite.change_x, sprite.change_y = PLAYER_MOVEMENT_SPEED*
                # if self.formation == 0:
                #     if count == 1:
                #         sprite.set_position(self.player_sprite.center_x, self.player_sprite.center_y+30*count)
                #
                #     else:
                #         sprite.set_position(self.player_sprite.center_x, self.player_sprite.center_y-15*count)
                # else:
                #     if self.player_sprite.character_face_direction == RIGHT_FACING:
                #         sprite.set_position(self.player_sprite.center_x-30*count, self.player_sprite.center_y)
                #     else:
                #         sprite.set_position(self.player_sprite.center_x+30*count, self.player_sprite.center_y)

        for engine in self.physics_engines:
            engine.update()

        self.player_sprites[0].on_update(delta_time)
        self.player_sprites[2].on_update(delta_time)

        # self.level_sprites.update()

        self.enemy_list.on_update(delta_time)

        '''Handle positioning the player's weapon'''
        dx = (self.mouse_position[0]*self.viewport_scale+arcade.get_viewport()[0])-self.player_sprite.center_x
        dy = (self.mouse_position[1]*self.viewport_scale+arcade.get_viewport()[2])-self.player_sprite.center_y
        angle = atan2(dy, dx)
        self.player_sprite.weapon.center_x = self.player_sprite.center_x+25*cos(angle)
        self.player_sprite.weapon.center_y = self.player_sprite.center_y+25*sin(angle)
        self.player_sprite.weapon.angle = degrees(angle)

        self.player_sprite.weapon.update_animation()



        player_stab = (
            self.player_sprite.weapon.is_stab and
            self.player_sprite.weapon.cur_stab_texture == 1
        )

        player_cut = (
            self.player_sprite.weapon.is_cut and
            self.player_sprite.weapon.cur_cut_texture == 1
        )

        if player_cut or player_stab:
            enemy_collisions = self.player_sprite.weapon.collides_with_list(
                self.enemy_list)
        else:
            enemy_collisions = []

        '''Check for enemy being hit'''
        if len(enemy_collisions) > 0:
            for enemy in enemy_collisions:
                print("LOL BRUH U JUST GOT HIT")
                enemy.is_hit = True
                enemy.health -= 10
        # print(self.player_sprite.weapon.collides_with_list(self.enemy_list))

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

        if key == arcade.key.EQUAL:
            self.viewport_scale -= 0.25
        if key == arcade.key.MINUS:
            self.viewport_scale += 0.25

        if key == arcade.key.Q:
            self.formation = not self.formation

        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            self.window.set_vsync(not self.window.vsync)

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

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = (x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.weapon.is_stab = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.weapon.is_cut = True


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
    # ship_view = ShipView()
    player_view = PlayerView()

    # window.show_view(ship_view)
    window.show_view(player_view)

    arcade.run()


if __name__ == "__main__":
    main()
