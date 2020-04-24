import arcade

from triple_vision import Settings as s
from triple_vision.triple_vision import TripleVision


class PlayButton(arcade.TextButton):

    def __init__(self, view, *args, **kwargs) -> None:
        super().__init__(text='Play', *args, **kwargs)
        self.view = view
        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.view.play()
            self.pressed = False


class MainView(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        self.play_button = None
        self.background = arcade.load_texture('assets/background.png')

    def play(self) -> None:
        self.window.button_list.clear()
        self.window.show_view(TripleVision())

    def on_show(self) -> None:
        self.play_button = PlayButton(
            self,
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2,
            width=120,
            height=60,
            font_color=arcade.color.BLACK
        )
        self.window.button_list.append(self.play_button)

    def on_draw(self) -> None:
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=s.WINDOW_SIZE[0],
            height=s.WINDOW_SIZE[1],
            texture=self.background
        )

        self.play_button.draw()
