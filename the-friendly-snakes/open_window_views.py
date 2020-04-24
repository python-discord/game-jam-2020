import arcade
from pyglet import gl
from Math import Maths
from StartMenu import StartMenuView

# help-phosphorus
# game-development

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "3 of a kind"

CHARACTER_SCALING = 1

PLAYER_MOVEMENT_SPEED = 10
PLAYER_JUMP_SPEED = 30
GRAVITY = 1.5

LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH / 2
BOTTOM_VIEWPORT_MARGIN = 128
TOP_VIEWPORT_MARGIN = 0

CAMERA_FOLLOW_SPEED = 0.2


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()

        self.window = None

        self.player_list = None
        self.background_list = None
        self.wall_list = None
        self.coin_list = None

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

    def on_show(self):

        self.window = arcade.get_window()

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.view_bottom = 0
        self.view_left = 0

        self.coin_counter = 0

        self.draw_shop_tip = False

        image_source = 'images/player_1/player_look_right.png'
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 600
        self.player_list.append(self.player_sprite)

        map_name = 'tmx_maps/map2.tmx'
        background_layer_name = 'Background'
        platforms_layer_name = 'Platforms'
        coins_layer_name = 'Coins'

        my_map = arcade.tilemap.read_tmx(map_name)

        self.background_list = arcade.tilemap.process_layer(my_map, background_layer_name)
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name)
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name)

        self.screen_width, self.screen_height = self.window.get_size()
        self.old_screen_center_x = int(self.screen_width / 2)
        self.old_screen_center_y = int(self.screen_height / 2)
        self.screen_center_x = int(self.screen_width / 2)
        self.screen_center_y = int(self.screen_height / 2)

        self.should_be_in_menu = False

        self.quit_button_color = [54, 155, 227, 255]
        self.quit_button = arcade.draw_text('Quit', self.screen_center_x, self.screen_center_y, arcade.csscolor.BLACK, 32, anchor_x='center', anchor_y='center')
        self.quit_button_box = arcade.create_rectangle_filled(0, 0, 170, 90, self.quit_button_color)

        self.pause_background = arcade.load_texture('images/backgrounds/pause_background.png')

        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()

        self.screen_width, self.screen_height = self.window.get_size()
        self.screen_center_x = int(self.screen_width / 2)
        self.screen_center_y = int(self.screen_height / 2)

        self.background_list.draw(filter=gl.GL_NEAREST)
        self.wall_list.draw(filter=gl.GL_NEAREST)

        if self.draw_shop_tip:
            shop_tip = 'Press E to open the shop'
            arcade.draw_text(shop_tip, 50, 1350, arcade.csscolor.BLACK, 32)

        self.player_list.draw(filter=gl.GL_NEAREST)
        self.coin_list.draw(filter=gl.GL_NEAREST)

        coin_text = f'Coins: {self.coin_counter}'
        arcade.draw_text(coin_text, self.view_left + 10, self.view_bottom + SCREEN_HEIGHT - 50, arcade.csscolor.BLACK, 32)

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
                                                32, anchor_x='center', anchor_y='center')
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
        if not self.should_be_in_menu:
            if key == arcade.key.A:
                self.left_pressed = True

            if key == arcade.key.D:
                self.right_pressed = True

            if key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    arcade.play_sound(self.jump_sound)

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

    def on_update(self, delta_time):
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.coin_counter += 1

        self.player_sprite.change_x = 0

        if not self.should_be_in_menu:
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

            if self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

            if self.player_sprite.left <= 600.0:
                self.draw_shop_tip = True
            else:
                self.draw_shop_tip = False

        self.view_left = int(arcade.lerp(self.view_left, self.player_sprite.center_x - SCREEN_WIDTH / 2, CAMERA_FOLLOW_SPEED))
        self.view_bottom = int(arcade.lerp(self.view_bottom, self.player_sprite.center_y - SCREEN_HEIGHT / 2, CAMERA_FOLLOW_SPEED))

        if not self.should_be_in_menu:
            arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    start_menu = StartMenuView()
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()