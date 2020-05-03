import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class StartMenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.window = None

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

        game_title_text = 'Flimsy Billy\'s Coin Dash 3: Super Duper Tag 3 Electric Tree'
        self.title_text = arcade.draw_text(game_title_text, self.screen_center_x, self.screen_center_y + 150,
                                                  anchor_x='center',
                                                  anchor_y='center', color=arcade.csscolor.WHITE, font_size=32)
        play_text = 'Play'
        self.play_button = play_text_sprite = arcade.draw_text(play_text, self.screen_center_x, self.screen_center_y,
                                                               anchor_x='center', anchor_y='center',
                                                               color=arcade.csscolor.WHITE, font_size=64)

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
            from open_window_views import MyGame
            game = MyGame(1, 0, 0)
            self.window.show_view(game)

    def on_draw(self):
        arcade.start_render()

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        screen_width, screen_height = self.window.get_size()
        self.screen_center_x = int(screen_width / 2)
        self.screen_center_y = int(screen_height / 2)

        if self.old_screen_center_x != self.screen_center_x or self.old_screen_center_y !=  self.screen_center_y:
            game_title_text = 'Flimsy Billy\'s Coin Dash 3: Super Duper Tag 3 Electric Tree'
            self.title_text = arcade.draw_text(game_title_text, self.screen_center_x, self.screen_center_y + 150,
                                               anchor_x='center',
                                               anchor_y='center', color=arcade.csscolor.WHITE, font_size=32)
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