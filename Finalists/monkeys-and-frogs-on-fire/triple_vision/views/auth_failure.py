import arcade

from triple_vision import Settings as s
from triple_vision.views.utils import BackButton


class AuthenticationFailure(arcade.View):

    def __init__(self, back_view, error) -> None:
        super().__init__()
        self.back_view = back_view
        self.error = error

        self.error_text = None
        self.back_button = None

        self.background = arcade.load_texture('assets/background.png')

    def back(self) -> None:
        self.window.button_list.clear()
        self.window.show_view(self.back_view)

    def on_show(self) -> None:
        self.error_text = arcade.draw_text(
            f'Error: {self.error.name}',
            start_x=s.WINDOW_SIZE[0] / 2,
            start_y=s.WINDOW_SIZE[1] / 2,
            color=arcade.color.WHITE,
            align='center',
            anchor_x='center',
            anchor_y='center',
            font_size=32
        )

        self.back_button = BackButton(
            self,
            clicked='assets/buttons/back_pressed.png',
            normal='assets/buttons/back_released.png',
            center_x=60,
            center_y=30,
            viewport=(0, 0)
        )

    def on_draw(self) -> None:
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=s.WINDOW_SIZE[0],
            height=s.WINDOW_SIZE[1],
            texture=self.background
        )

        self.error_text.draw()
        self.back_button.draw()

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        self.back_button.check_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        self.back_button.check_mouse_release(x, y, button, modifiers)
