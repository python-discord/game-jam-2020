import arcade
from pyglet import gl

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


class Maths():

    @classmethod
    def lerp(cls, v1: float, v2: float, u: float):
        return v1 + ((v2 - v1) * u)

    @classmethod
    def clamp(cls, x: float, lowerlimit: float, upperlimit: float):
        if x < lowerlimit:
            x = lowerlimit
        if x > upperlimit:
            x = upperlimit
        return x

    @classmethod
    def smoothstep(cls, edge0: float, edge1: float, x: float):
        x = Maths.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return x * x * x * (x * (x * 6 - 15) + 10)

    @classmethod
    def lowlimit(cls, x, lowerlimit):
        if x < lowerlimit:
            x = lowerlimit
        return x

    @classmethod
    def maxlimit(cls, x, upperlimit):
        if x > upperlimit:
            x = upperlimit
        return x


class StartMenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.wnidow = None

        self.hover_color = [0, 0, 0, 100]
        self.click_color = [0, 0, 0, 150]

        self.hovering = None
        self.clicking = None

        self.draw_play_button_hover = None

        self.play_bottom = None
        self.play_left = None

        self.title_text = None
        self.play_button = None

        self.old_screen_center_x = None
        self.old_screen_center_y = None
        self.screen_center_x = None
        self.screen_center_y = None

    def on_show(self):

        self.window = arcade.get_window()

        self.draw_play_button_hover = False

        self.hovering = False
        self.clicking = False

        self.old_screen_center_x = int(self.window.get_size()[0] / 2)
        self.old_screen_center_y = int(self.window.get_size()[1] / 2)
        self.screen_center_x = int(self.window.get_size()[0] / 2)
        self.screen_center_y = int(self.window.get_size()[1] / 2)

        game_title_text = 'Three of a Kind'
        self.title_text = arcade.draw_text(game_title_text, self.screen_center_x, self.screen_center_y + 150,
                                                  anchor_x='center',
                                                  anchor_y='center', color=arcade.csscolor.WHITE, font_size=64)
        play_text = 'Play'
        self.play_button = play_text_sprite = arcade.draw_text(play_text, self.screen_center_x, self.screen_center_y, anchor_x='center',
                                            anchor_y='center', color=arcade.csscolor.WHITE, font_size=64)

        arcade.set_background_color([66, 245, 212, 255])

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.play_left + 134 + 50 >= x >= self.play_left - 50 and self.play_bottom + 80 + 25 >= y >= self.play_bottom - 25:
            self.draw_play_button_hover = True
            self.hovering = True
        else:
            self.draw_play_button_hover = False
            self.hovering = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_left + 134 + 50 >= x >= self.play_left - 50 and self.play_bottom + 80 + 25 >= y >= self.play_bottom - 25:
            self.draw_play_button_hover = True
            self.clicking = True
        else:
            self.draw_play_button_hover = False
            self.clicking = False

    def on_mouse_release(self, x, y, button, modifiers):
        if self.play_left + 134 + 50 >= x >= self.play_left - 50 and self.play_bottom + 80 + 25 >= y >= self.play_bottom - 25:
            game = MyGame()
            self.window.show_view(game)

    def on_draw(self):
        arcade.start_render()

        screen_width, screen_height = self.window.get_size()
        self.screen_center_x = int(screen_width / 2)
        self.screen_center_y = int(screen_height / 2)

        if self.old_screen_center_x != self.screen_center_x or self.old_screen_center_y !=  self.screen_center_y:
            game_title_text = 'Three of a Kind'
            self.title_text = arcade.draw_text(game_title_text, self.screen_center_x, self.screen_center_y + 150,
                                               anchor_x='center',
                                               anchor_y='center', color=arcade.csscolor.WHITE, font_size=64)
            play_text = 'Play'
            self.play_button = play_text_sprite = arcade.draw_text(play_text, self.screen_center_x,
                                                                   self.screen_center_y, anchor_x='center',
                                                                   anchor_y='center', color=arcade.csscolor.WHITE,
                                                                   font_size=64)

        self.old_screen_center_x = self.screen_center_x
        self.old_screen_center_y = self.screen_center_y

        if self.draw_play_button_hover:
            if self.clicking:
                arcade.draw_rectangle_filled(self.screen_center_x, self.screen_center_y, 234, 130, self.click_color)
            elif self.hovering:
                arcade.draw_rectangle_filled(self.screen_center_x, self.screen_center_y, 234, 130, self.hover_color)

        self.play_bottom = self.play_button.bottom
        self.play_left = self.play_button.left

        self.title_text.draw()
        self.play_button.draw()


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()

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

    def on_show(self):
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

        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()

        self.background_list.draw(filter=gl.GL_NEAREST)
        self.wall_list.draw(filter=gl.GL_NEAREST)

        if self.draw_shop_tip:
            shop_tip = 'Press E to open the shop'
            arcade.draw_text(shop_tip, 50, 1350, arcade.csscolor.BLACK, 32)

        self.player_list.draw(filter=gl.GL_NEAREST)
        self.coin_list.draw(filter=gl.GL_NEAREST)

        coin_text = f'Coins: {self.coin_counter}'
        arcade.draw_text(coin_text, self.view_left + 10, self.view_bottom + SCREEN_HEIGHT - 50, arcade.csscolor.BLACK, 32)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.left_pressed = True

        if key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)

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

        arcade.set_viewport(self.view_left, self.view_left + SCREEN_WIDTH, self.view_bottom, self.view_bottom + SCREEN_HEIGHT)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    start_menu = StartMenuView()
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()