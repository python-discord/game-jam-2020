import arcade

from triple_vision import Settings as s
# from triple_vision.networking import client


class BackButton(arcade.TextButton):

    def __init__(self, view, *args, **kwargs) -> None:
        super().__init__(text='Back', *args, **kwargs)
        self.view = view
        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.view.back()
            self.pressed = False


class LeaderboardView(arcade.View):

    def __init__(self, main_view: arcade.View) -> None:
        super().__init__()

        self.main_view = main_view

        self.back_button = None
        self.game_title = None
        self.background = arcade.load_texture('assets/background.png')

    def back(self) -> None:
        self.window.button_list.clear()
        self.window.show_view(self.main_view)

    def on_show(self) -> None:
        self.back_button = BackButton(
            self,
            center_x=60,
            center_y=30,
            width=120,
            height=60,
            font_color=arcade.color.BLACK
        )
        self.window.button_list.append(self.back_button)

        self.game_title = arcade.draw_text(
            text='Triple Vision',
            start_x=s.WINDOW_SIZE[0] / 2,
            start_y=s.WINDOW_SIZE[1] / 8 * 7,
            color=arcade.color.WHITE,
            font_size=42,
            align='center',
            anchor_x='center',
            anchor_y='center'
        )

    def on_draw(self) -> None:
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=s.WINDOW_SIZE[0],
            height=s.WINDOW_SIZE[1],
            texture=self.background
        )

        self.back_button.draw()
        self.game_title.draw()
