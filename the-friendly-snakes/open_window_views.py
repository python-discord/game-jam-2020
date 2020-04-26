import arcade
from pyglet import gl
from StartMenu import StartMenuView
import random
from GameOver import GameOver

# help-phosphorus
# game-development

GAME_OVER = GameOver()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "3 of a kind"

CHARACTER_SCALING = 1
POTION_SCALING = 5

PLAYER_MOVEMENT_SPEED = 15
PLAYER_JUMP_SPEED = 30
GRAVITY = 1.5

UPDATES_PER_FRAME = 5

RIGHT_FACING = 0
LEFT_FACING = 1

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
BOTTOM_VIEWPORT_MARGIN = 128
TOP_VIEWPORT_MARGIN = 0

CAMERA_FOLLOW_SPEED = 0.2

FIRST_TIME = 0
SECOND_TIME = 1


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class PlayerCharacter(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        self.cur_texture = 0

        main_path = 'images/player_1/'
        
        self.idle_texture_pair = load_texture_pair(f'{main_path}/player_idle.png')

        self.walk_textures = []
        for i in range(6):
            texture = load_texture_pair(f'{main_path}walk_{i}.png')
            self.walk_textures.append(texture)

        self.texture = self.idle_texture_pair[RIGHT_FACING]

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 5 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]


class Potion(arcade.Sprite):
    def __init__(self, potion_path, potions_in_anim):
        super().__init__()

        self.path = potion_path
        self.cur_texture = 0
        self.num_of_potion_frames = potions_in_anim

        self.potion_textures = []
        for i in range(self.num_of_potion_frames):
            texture = arcade.load_texture(f'{potion_path}/{i}.png')
            self.potion_textures.append(texture)

        self.texture = self.potion_textures[0]

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture > (self.num_of_potion_frames - 1) * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.potion_textures[self.cur_texture // UPDATES_PER_FRAME]


class MyGame(arcade.View):
    def __init__(self, run, previous_time):
        super().__init__()

        self.window = None

        self.game_timer = 0
        self.previous_time = previous_time
        self.run = run
        self.drew_game_over = False

        self.music = arcade.load_sound('Music/The 16Bit Cowboy.wav')
        self.music_length = 59
        self.musicdt = 0

        self.player_list = None
        self.background_list = None
        self.wall_list = None
        self.dont_touch_list = None
        self.super_lava = None
        self.coin_list = None
        self.coin_2_list = None
        self.coin_5_list = None
        self.coin_secret_list = None
        self.ladder_list = None
        self.ignore_list = None
        self.portal_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.left_pressed = False
        self.right_pressed = False

        self.view_bottom = 0
        self.view_left = 0

        self.coin_counter = 0

        self.collect_coin_sound = arcade.load_sound('sounds/coin2.wav')
        self.jump_sound = arcade.load_sound('sounds/jump.wav')

        self.draw_shop_tip = False
        self.draw_back_tip = False
        self.draw_jungle_tp = False
        self.draw_door_1_tip = False
        self.draw_door_2_tip = False
        self.draw_door_3_tip = False
        self.draw_potion_1_tip = False
        self.draw_potion_2_tip = False
        self.draw_potion_3_tip = False
        self.draw_secret_tip = False
        self.draw_portal_tip = False

        self.delta_track = 0

        self.got_potion_3 = False
        self.delta_track2 = 0

        self.should_be_in_menu = None

        self.old_screen_center_x = None
        self.old_screen_center_y = None
        self.screen_center_x = None
        self.screen_center_y = None
        self.screen_width = None
        self.screen_height = None

        self.quit_button = None
        self.quit_button_box = None
        self.quit_button_color = None

        self.pause_background = None

        self.potion_list = None


    def on_show(self):

        self.window = arcade.get_window()

        self.game_timer = 0
        self.drew_game_over = False

        self.music.play(volume=0.01)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.coin_2_list = arcade.SpriteList()
        self.coin_5_list = arcade.SpriteList()
        self.potion_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()

        self.coin_counter = 0
        self.delta_track = 0

        self.got_potion_3 = False
        self.delta_track2 = 0

        self.draw_shop_tip = False
        self.draw_back_tip = False
        self.draw_jungle_tp = False
        self.draw_door_1_tip = False
        self.draw_door_2_tip = False
        self.draw_door_3_tip = False
        self.draw_potion_1_tip = False
        self.draw_potion_2_tip = False
        self.draw_potion_3_tip = False
        self.draw_secret_tip = False

        potion_path = 'images/items/jump_boost_potion'
        potions_in_anim = 6
        potion = Potion(potion_path, potions_in_anim)
        potion.center_x = 89 * 96 + 48
        potion.center_y = 20 * 96 - 48
        self.potion_list.append(potion)

        potion_path = 'images/items/speed_boost_potion'
        potions_in_anim = 5
        potion = Potion(potion_path, potions_in_anim)
        potion.center_x = 89 * 96 + 48
        potion.center_y = 25 * 96 - 48
        self.potion_list.append(potion)

        potion_path = 'images/items/tp_and_freeze_potion'
        potions_in_anim = 7
        potion = Potion(potion_path, potions_in_anim)
        potion.center_x = 89 * 96 + 48
        potion.center_y = 30 * 96 - 48
        self.potion_list.append(potion)

        path = 'images/items/Portal'
        frames_in_anim = 9
        portal = Potion(path, frames_in_anim)
        portal.center_x = 71 * 96 + 48
        portal.center_y = 29 * 96 + 48
        self.portal_list.append(portal)

        map_name = 'tmx_maps/map2.tmx'
        background_layer_name = 'Background'
        platforms_layer_name = 'Platforms'
        coins_layer_name = 'Coins'
        coins_2_layer_name = 'Coins2'
        coins_5_layer_name = 'Coins5'
        secret_coins_layer_name = 'SuperSecret'
        ladder_layer_name = 'Ladders'
        dont_touch_layer_name = 'Dont Touch'
        super_lava_layer_name = 'SuperLava'
        ignore_layer_name = 'ig'

        my_map = arcade.tilemap.read_tmx(map_name)

        self.background_list = arcade.tilemap.process_layer(my_map, background_layer_name)
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name)
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name)
        self.coin_2_list = arcade.tilemap.process_layer(my_map, coins_2_layer_name)
        self.coin_5_list = arcade.tilemap.process_layer(my_map, coins_5_layer_name)
        self.coin_secret_list = arcade.tilemap.process_layer(my_map, secret_coins_layer_name)
        self.ladder_list = arcade.tilemap.process_layer(my_map, ladder_layer_name)
        self.dont_touch_list = arcade.tilemap.process_layer(my_map, dont_touch_layer_name)
        self.super_lava = arcade.tilemap.process_layer(my_map, super_lava_layer_name)
        self.ignore_list = arcade.tilemap.process_layer(my_map, ignore_layer_name)

        self.screen_width, self.screen_height = self.window.get_size()
        self.old_screen_center_x = int(self.screen_width / 2)
        self.old_screen_center_y = int(self.screen_height / 2)
        self.screen_center_x = int(self.screen_width / 2)
        self.screen_center_y = int(self.screen_height / 2)

        self.should_be_in_menu = False

        self.quit_button_color = [54, 155, 227, 255]
        self.quit_button = arcade.draw_text('Quit', self.screen_center_x, self.screen_center_y, arcade.csscolor.BLACK, 32, anchor_x='center', anchor_y='center', font_name='fonts/RobotoMono-Regular.ttf')
        self.quit_button_box = arcade.create_rectangle_filled(0, 0, 170, 90, self.quit_button_color)

        self.pause_background = arcade.load_texture('images/backgrounds/pause_background.png')

        self.background_list.draw(filter=gl.GL_NEAREST)
        self.ignore_list.draw(filter=gl.GL_NEAREST)
        self.dont_touch_list.draw(filter=gl.GL_NEAREST)
        self.super_lava.draw(filter=gl.GL_NEAREST)
        self.wall_list.draw(filter=gl.GL_NEAREST)
        self.ladder_list.draw(filter=gl.GL_NEAREST)
        self.potion_list.draw(filter=gl.GL_NEAREST)
        self.portal_list.draw(filter=gl.GL_NEAREST)
        self.player_list.draw(filter=gl.GL_NEAREST)
        self.coin_list.draw(filter=gl.GL_NEAREST)
        self.coin_2_list.draw(filter=gl.GL_NEAREST)
        self.coin_5_list.draw(filter=gl.GL_NEAREST)
        self.coin_secret_list.draw(filter=gl.GL_NEAREST)

        image_source = 'images/player_1/player_idle.png'
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 40 * 96
        self.player_sprite.center_y = 15 * 96
        self.player_list.append(self.player_sprite)

        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)

        self.view_left = self.player_sprite.center_x - SCREEN_WIDTH / 2
        self.view_bottom = self.player_sprite.center_y - SCREEN_HEIGHT / 2

        arcade.set_viewport(self.player_sprite.center_x - SCREEN_WIDTH / 2, self.player_sprite.center_x + SCREEN_WIDTH / 2, self.player_sprite.center_y - SCREEN_HEIGHT / 2,
                            self.player_sprite.center_y + SCREEN_HEIGHT / 2)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY, ladders=self.ladder_list)

    def on_draw(self):
        arcade.start_render()

        self.screen_width, self.screen_height = self.window.get_size()
        self.screen_center_x = int(self.screen_width / 2)
        self.screen_center_y = int(self.screen_height / 2)

        self.background_list.draw(filter=gl.GL_NEAREST)
        self.ignore_list.draw(filter=gl.GL_NEAREST)
        self.dont_touch_list.draw(filter=gl.GL_NEAREST)
        self.wall_list.draw(filter=gl.GL_NEAREST)


        if self.draw_shop_tip:
            shop_tip = 'Press E to open the shop'
            arcade.draw_text(shop_tip, 31 * 96 + 48, 17 * 96 - 48, arcade.csscolor.BLACK, 32, font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_back_tip:
            shop_tip = 'Press E to go back'
            arcade.draw_text(shop_tip, 88 * 96 + 48, 17 * 96 - 48, arcade.csscolor.BLACK, 32, font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_jungle_tp:
            tip = 'Press E to Enter'
            arcade.draw_text(tip, 74 * 96, 24 * 96 - 48, arcade.csscolor.WHITE, 32, font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_door_1_tip:
            tip = 'Press E to Enter'
            arcade.draw_text(tip, 86 * 96, 60 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_door_2_tip:
            tip = 'Press E to Enter'
            arcade.draw_text(tip, 91 * 96, 60 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_door_3_tip:
            tip = 'Press E to Enter'
            arcade.draw_text(tip, 96 * 96, 60 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_potion_1_tip:
            tip = 'Press E to Buy Speed Boost for 5 Coins'
            arcade.draw_text(tip, 84 * 96 + 48, 21 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_potion_2_tip:
            tip = 'Press E to Buy Jump Boost for 5 Coins'
            arcade.draw_text(tip, 84 * 96 + 48, 26 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_potion_3_tip:
            tip = 'Press E to Buy Secret Potion for 7 Coins'
            arcade.draw_text(tip, 84 * 96 + 48, 31 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_secret_tip:
            tip = 'Press E to Enter'
            arcade.draw_text(tip, 81 * 96 + 48, 4 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        if self.draw_portal_tip:
            tip = 'Press E to Enter'
            arcade.draw_text(tip, 69 * 96 + 48, 32 * 96 - 48, arcade.csscolor.WHITE, 32,
                             font_name='fonts/RobotoMono-Regular.ttf')

        self.super_lava.draw(filter=gl.GL_NEAREST)
        self.ladder_list.draw(filter=gl.GL_NEAREST)
        self.potion_list.draw(filter=gl.GL_NEAREST)
        self.portal_list.draw(filter=gl.GL_NEAREST)
        self.player_list.draw(filter=gl.GL_NEAREST)
        self.coin_list.draw(filter=gl.GL_NEAREST)
        self.coin_2_list.draw(filter=gl.GL_NEAREST)
        self.coin_5_list.draw(filter=gl.GL_NEAREST)
        self.coin_secret_list.draw(filter=gl.GL_NEAREST)

        coin_text = f'Coins: {self.coin_counter}'
        arcade.draw_text(coin_text, self.view_left + 10, self.view_bottom + SCREEN_HEIGHT - 50, arcade.csscolor.BLACK, 32, font_name='fonts/RobotoMono-Regular.ttf')

        timer_text = f'Time: {int(self.game_timer)}'
        arcade.draw_text(timer_text, self.view_left + 10, self.view_bottom + SCREEN_HEIGHT - 100, arcade.csscolor.BLACK,
                         32, font_name='fonts/RobotoMono-Regular.ttf')

        if self.previous_time > 0:
            timer_text = f'Previous Time: {int(self.previous_time)}'
            arcade.draw_text(timer_text, self.view_left + 10, self.view_bottom + SCREEN_HEIGHT - 150,
                             arcade.csscolor.BLACK,
                             32, font_name='fonts/RobotoMono-Regular.ttf')

        if self.should_be_in_menu:
            l, w, b, h = arcade.get_viewport()
            sw, sh = arcade.get_window().get_size()
            arcade.set_viewport(0, sw, 0,
                                sh)
            arcade.draw_lrwh_rectangle_textured(0, 0, sw, sh, self.pause_background)
            self.quit_button_box = arcade.create_rectangle_filled(w / 2,
                                                h / 2, width=300, height=50,
                                                                  color=self.quit_button_color)
            self.quit_button = arcade.draw_text('Quit', w / 2,
                                                h / 2, arcade.csscolor.BLACK,
                                                32, anchor_x='center', anchor_y='center', font_name='fonts/RobotoMono-Regular.ttf')
            self.quit_button_box.draw()
            self.quit_button.draw()

        self.old_screen_center_x = int(self.screen_width / 2)
        self.old_screen_center_y = int(self.screen_height / 2)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.should_be_in_menu:
            l, w, b, h = arcade.get_viewport()
            left = w / 2 - 150
            right = w / 2 + 150
            top = h / 2 + 25
            bottom = h / 2 - 25

            if bottom <= y <= top and left <= x <= right:
                self.quit_button_color = [54, 138, 199, 255]
            else:
                self.quit_button_color = [54, 155, 227, 255]

    def on_mouse_press(self, x, y, button, modifiers):
        if self.should_be_in_menu:
            l, w, b, h = arcade.get_viewport()
            left = w / 2 - 150
            right = w / 2 + 150
            top = h / 2 + 25
            bottom = h / 2 - 25

            if bottom <= y <= top and left <= x <= right:
                self.quit_button_color = [46, 114, 163, 255]
            else:
                self.quit_button_color = [54, 155, 227, 255]

    def on_mouse_release(self, x, y, button, modifiers):
        if self.should_be_in_menu:
            l, w, b, h = arcade.get_viewport()
            left = w / 2 - 150
            right = w / 2 + 150
            top = h / 2 + 25
            bottom = h / 2 - 25

            if bottom <= y <= top and left <= x <= right:
                self.window.close()

    def on_key_press(self, key, modifiers):
        global  PLAYER_JUMP_SPEED
        global  PLAYER_MOVEMENT_SPEED

        if not self.should_be_in_menu:
            if key == arcade.key.A:
                self.left_pressed = True

            if key == arcade.key.D:
                self.right_pressed = True

            if key == arcade.key.W:
                if self.physics_engine.is_on_ladder():
                    self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
                elif self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    arcade.play_sound(self.jump_sound)

            if key == arcade.key.S:
                if self.physics_engine.is_on_ladder():
                    self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

            if self.draw_shop_tip:
                if key == arcade.key.E:
                    self.player_sprite.center_x = 89 * 96
                    self.player_sprite.center_y = 15 * 96
                    self.view_left = self.player_sprite.center_x - SCREEN_WIDTH / 2
                    self.view_bottom = self.player_sprite.center_y - SCREEN_HEIGHT / 2
                    arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom,
                                        self.view_bottom + SCREEN_HEIGHT)

            if self.draw_back_tip:
                if key == arcade.key.E:
                    self.player_sprite.center_x = 33 * 96
                    self.player_sprite.center_y = 15 * 96
                    self.view_left = self.player_sprite.center_x - SCREEN_WIDTH / 2
                    self.view_bottom = self.player_sprite.center_y - SCREEN_HEIGHT / 2
                    arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom,
                                        self.view_bottom + SCREEN_HEIGHT)

            if self.draw_jungle_tp:
                if key == arcade.key.E:
                    self.player_sprite.center_x = 81 * 96
                    self.player_sprite.center_y = 59 * 96
                    self.view_left = self.player_sprite.center_x - SCREEN_WIDTH / 2
                    self.view_bottom = self.player_sprite.center_y - SCREEN_HEIGHT / 2
                    arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom,
                                        self.view_bottom + SCREEN_HEIGHT)

            if self.draw_door_1_tip or self.draw_door_2_tip or self.draw_door_3_tip:
                if key == arcade.key.E:
                    self.player_sprite.center_x = 74.5 * 96
                    self.player_sprite.center_y = 23 * 96
                    self.view_left = self.player_sprite.center_x - SCREEN_WIDTH / 2
                    self.view_bottom = self.player_sprite.center_y - SCREEN_HEIGHT / 2
                    arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom,
                                        self.view_bottom + SCREEN_HEIGHT)
                    if random.randint(0, 100) < 33:
                        self.coin_counter = self.coin_counter // 2

            if self.draw_potion_1_tip:
                if key == arcade.key.E:
                    if self.coin_counter >= 5:
                        PLAYER_MOVEMENT_SPEED += 2
                        self.coin_counter -= 5

            if self.draw_potion_2_tip:
                if key == arcade.key.E:
                    if self.coin_counter >= 5:
                        PLAYER_JUMP_SPEED += 1
                        self.coin_counter -= 5

            if self.draw_potion_3_tip:
                if key == arcade.key.E:
                    if self.coin_counter >= 7:
                        self.got_potion_3 = True
                        self.coin_counter -= 7
                        self.player_sprite.center_x = 70 * 96 + 48
                        self.player_sprite.center_y = 8 * 96
                        self.view_left = self.player_sprite.center_x - SCREEN_WIDTH / 2
                        self.view_bottom = self.player_sprite.center_y - SCREEN_HEIGHT / 2
                        arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom,
                                            self.view_bottom + SCREEN_HEIGHT)

            if self.draw_secret_tip:
                if key == arcade.key.E:
                    self.player_sprite.center_x = 33 * 96
                    self.player_sprite.center_y = 15 * 96
                    self.view_left = self.player_sprite.center_x - SCREEN_WIDTH / 2
                    self.view_bottom = self.player_sprite.center_y - SCREEN_HEIGHT / 2
                    arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom,
                                        self.view_bottom + SCREEN_HEIGHT)

            if self.draw_portal_tip:
                if key == arcade.key.E:
                    window = arcade.get_window()
                    next_game = MyGame(2, self.game_timer)
                    window.show_view(next_game)

        if key == arcade.key.ESCAPE:
            if self.should_be_in_menu:
                self.should_be_in_menu = False
            else:
                self.should_be_in_menu = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = False

        if key == arcade.key.D:
            self.right_pressed = False

        if key == arcade.key.S:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0

        if key == arcade.key.W:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.game_timer += delta_time

        self.musicdt += delta_time
        if self.musicdt >= self.music_length:
            self.music.play(volume=0.01)

        self.delta_track += delta_time
        if self.delta_track >= 5:
            if self.coin_counter >= 1:
                self.coin_counter -= 1
            self.delta_track = 0

        if self.got_potion_3:
            self.delta_track2 += delta_time
            if self.delta_track2 >= 1:
                for lava in self.super_lava:
                    if lava.right < 96 * 105:
                        lava.change_x = 5
                self.delta_track2 = 0

        self.super_lava.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        coin_2_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_2_list)
        coin_5_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_5_list)
        coin_secret_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_secret_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.coin_counter += 1

        for coin in coin_2_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.coin_counter += 2

        for coin in coin_5_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.coin_counter += 5

        for coin in coin_secret_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.coin_counter += 5

        self.player_sprite.change_x = 0

        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = 40 * 96
            self.player_sprite.center_y = 15 * 96

            self.coin_counter = self.coin_counter // 2

        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.super_lava):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = 40 * 96
            self.player_sprite.center_y = 15 * 96

            self.coin_counter = self.coin_counter // 2

        if not self.should_be_in_menu:
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

            if self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

            # Go To Shop
            if self.player_sprite.right <= 96 * 37 and self.player_sprite.left >= 31 * 96 and self.player_sprite.top <= 16 * 96 and self.player_sprite.bottom >= 12 * 96:
                self.draw_shop_tip = True
            else:
                self.draw_shop_tip = False

            # Leave Shop
            if self.player_sprite.left >= 88 * 96 and self.player_sprite.right <= 94 * 96 and self.player_sprite.top <= 16 * 96 and self.player_sprite.bottom >= 12 * 96:
                self.draw_back_tip = True
            else:
                self.draw_back_tip = False

            # Go To Jungle Secret Thing
            if self.player_sprite.left >= 73 * 96 and self.player_sprite.right <= 79 * 96 and self.player_sprite.top <= 24 * 96 and self.player_sprite.bottom >= 21 * 96:
                self.draw_jungle_tp = True
            else:
                self.draw_jungle_tp = False

            # Go Away From Jungle 1
            if self.player_sprite.left >= 85 * 96 and self.player_sprite.right <= 90 * 96 and self.player_sprite.top <= 62 * 96 and self.player_sprite.bottom >= 57 * 96:
                self.draw_door_1_tip = True
            else:
                self.draw_door_1_tip = False

            # Go Away From Jungle 2
            if self.player_sprite.left >= 90 * 96 and self.player_sprite.right <= 95 * 96 and self.player_sprite.top <= 62 * 96 and self.player_sprite.bottom >= 57 * 96:
                self.draw_door_2_tip = True
            else:
                self.draw_door_2_tip = False

            # Go Away From Jungle 3
            if self.player_sprite.left >= 96 * 96 and self.player_sprite.right <= 100 * 96 and self.player_sprite.top <= 62 * 96 and self.player_sprite.bottom >= 57 * 96:
                self.draw_door_3_tip = True
            else:
                self.draw_door_3_tip = False

            # Get Potion 1
            if self.player_sprite.left >= 88 * 96 and self.player_sprite.right <= 94 * 96 and self.player_sprite.top <= 21 * 96 and self.player_sprite.bottom >= 18 * 96:
                self.draw_potion_1_tip = True
            else:
                self.draw_potion_1_tip = False

            # Get Potion 2
            if self.player_sprite.left >= 88 * 96 and self.player_sprite.right <= 94 * 96 and self.player_sprite.top <= 26 * 96 and self.player_sprite.bottom >= 23 * 96:
                self.draw_potion_2_tip = True
            else:
                self.draw_potion_2_tip = False

            # Get Potion 3
            if self.player_sprite.left >= 88 * 96 and self.player_sprite.right <= 94 * 96 and self.player_sprite.top <= 31 * 96 and self.player_sprite.bottom >= 28 * 96:
                self.draw_potion_3_tip = True
            else:
                self.draw_potion_3_tip = False

            # Secret Tip
            if self.player_sprite.left >= 83 * 96 and self.player_sprite.top <= 4 * 96 and self.player_sprite.bottom >= 0:
                self.draw_secret_tip = True
            else:
                self.draw_secret_tip = False

            # Go To Second Part
            if self.player_sprite.left >= 69 * 96 and self.player_sprite.right <= 74 * 96 and self.player_sprite.top <= 32 * 96 and self.player_sprite.bottom >= 27 * 96:
                self.draw_portal_tip = True
            else:
                self.draw_portal_tip = False

            if self.game_timer >= self.previous_time and self.run == 2 and not self.drew_game_over:
                window = arcade.get_window()
                window.show_view(GAME_OVER)

        self.player_list.update_animation()
        self.potion_list.update_animation()
        self.portal_list.update_animation()

        self.view_left = int(arcade.lerp(self.view_left, self.player_sprite.center_x - SCREEN_WIDTH / 2, CAMERA_FOLLOW_SPEED))
        self.view_bottom = int(arcade.lerp(self.view_bottom, self.player_sprite.center_y - SCREEN_HEIGHT / 2, CAMERA_FOLLOW_SPEED))

        if not self.should_be_in_menu:
            arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)


def main(gm=False):
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    start_menu = StartMenuView()
    game = MyGame(2, 5)
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()
