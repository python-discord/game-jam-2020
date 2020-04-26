import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class GameOver(arcade.View):
    def __init__(self):
        self.window = None

        self.hover_color = [0, 0, 0, 100]
        self.click_color = [0, 0, 0, 150]

        self.hovering = None
        self.clicking = None

        self.draw_restart_button_hover = None

        self.restart_bottom = None
        self.restart_left = None

        self.game_over_text = None
        self.game_over_text2 = None
        self.restart_button = None

        self.old_screen_center_x = None
        self.old_screen_center_y = None
        self.screen_center_x = None
        self.screen_center_y = None

    def on_show(self):

        self.window = arcade.get_window()

        self.draw_restart_button_hover = False

        self.hovering = False
        self.clicking = False

        self.old_screen_center_x = int(self.window.get_size()[0] / 2)
        self.old_screen_center_y = int(self.window.get_size()[1] / 2)
        self.screen_center_x = int(self.window.get_size()[0] / 2)
        self.screen_center_y = int(self.window.get_size()[1] / 2)

        game_over_text = 'Game Over!'
        self.game_over_text = arcade.draw_text(game_over_text, self.screen_center_x, self.screen_center_y + 150,
                                           anchor_x='center',
                                           anchor_y='center', color=arcade.csscolor.WHITE, font_size=32, font_name='fonts/RobotoMono-Regular.ttf')
        game_over_text = 'You Couldn\'t Get More Coins Than You Did On The Bar-Round!'
        self.game_over_text2 = arcade.draw_text(game_over_text, self.screen_center_x, self.screen_center_y + 100,
                                                anchor_x='center',
                                                anchor_y='center', color=arcade.csscolor.WHITE, font_size=32,
                                                font_name='fonts/RobotoMono-Regular.ttf')

        restart_text = 'Restart'
        self.restart_button = arcade.draw_text(restart_text, self.screen_center_x, self.screen_center_y,
                                                               anchor_x='center', anchor_y='center',
                                                               color=arcade.csscolor.WHITE, font_size=64, font_name='fonts/RobotoMono-Regular.ttf')

        arcade.set_background_color([66, 245, 212, 255])

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.play_left + self.restart_button.width + 50 >= x >= self.play_left - 50 and self.play_bottom + self.restart_button.height + 25 >= y >= self.play_bottom - 25:
            self.draw_restart_button_hover = True
            self.hovering = True
        else:
            self.draw_restart_button_hover = False
            self.hovering = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_left + self.restart_button.width + 50 >= x >= self.play_left - 50 and self.play_bottom + self.restart_button.height + 25 >= y >= self.play_bottom - 25:
            self.draw_restart_button_hover = True
            self.clicking = True
        else:
            self.draw_restart_button_hover = False
            self.clicking = False

    def on_mouse_release(self, x, y, button, modifiers):
        if self.play_left + self.restart_button.width + 50 >= x >= self.play_left - 50 and self.play_bottom + self.restart_button.height + 25 >= y >= self.play_bottom - 25:
            from open_window_views import MyGame
            game = MyGame(1, 0, 0)
            self.window.show_view(game)

    def on_draw(self):
        arcade.start_render()

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        screen_width, screen_height = self.window.get_size()
        self.screen_center_x = int(screen_width / 2)
        self.screen_center_y = int(screen_height / 2)

        if self.old_screen_center_x != self.screen_center_x or self.old_screen_center_y != self.screen_center_y:
            game_over_text = 'Game Over!'
            self.game_over_text = arcade.draw_text(game_over_text, self.screen_center_x, self.screen_center_y + 150,
                                               anchor_x='center',
                                               anchor_y='center', color=arcade.csscolor.WHITE, font_size=32,
                                               font_name='fonts/RobotoMono-Regular.ttf')
            game_over_text = 'You Couldn\'t Get More Coins Than You Did On The Bar-Round!'
            self.game_over_text2 = arcade.draw_text(game_over_text, self.screen_center_x, self.screen_center_y + 100,
                                                   anchor_x='center',
                                                   anchor_y='center', color=arcade.csscolor.WHITE, font_size=32,
                                                   font_name='fonts/RobotoMono-Regular.ttf')

            restart_text = 'Restart'
            self.restart_button = arcade.draw_text(restart_text, self.screen_center_x,
                                                                   self.screen_center_y,
                                                                   anchor_x='center', anchor_y='center',
                                                                   color=arcade.csscolor.WHITE, font_size=64,
                                                                   font_name='fonts/RobotoMono-Regular.ttf')

        self.old_screen_center_x = self.screen_center_x
        self.old_screen_center_y = self.screen_center_y

        if self.draw_restart_button_hover:
            if self.clicking:
                arcade.draw_rectangle_filled(self.screen_center_x, self.screen_center_y, self.restart_button.width + 100, self.restart_button.height + 50, self.click_color)
            elif self.hovering:
                arcade.draw_rectangle_filled(self.screen_center_x, self.screen_center_y, self.restart_button.width + 100, self.restart_button.height + 50, self.hover_color)

        self.play_bottom = self.restart_button.bottom
        self.play_left = self.restart_button.left

        self.game_over_text.draw()
        self.game_over_text2.draw()
        self.restart_button.draw()

def main(gm=False):
    if not gm:
        window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Help', resizable=True)
        window.show_view(GameOver())
        arcade.run()

if __name__ == "__main__":
    main()