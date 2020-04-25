import arcade

from triple_vision import Settings as s
from triple_vision.triple_vision import TripleVision
from triple_vision.views.leaderboard_view import LeaderboardView


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


class LeaderboardButton(arcade.TextButton):

    def __init__(self, view, *args, **kwargs) -> None:
        super().__init__(text='Leaderboard', *args, **kwargs)
        self.view = view
        self.pressed = False

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.view.leaderboard()
            self.pressed = False


class MainView(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        self.play_button = None
        self.leaderboard_button = None

        self.game_title = None

        self.background = arcade.load_texture('assets/background.png')

    def play(self) -> None:
        self.window.button_list.clear()
        self.window.show_view(TripleVision())

    def leaderboard(self) -> None:
        self.window.button_list.clear()
        self.window.show_view(LeaderboardView(self))

    def on_show(self) -> None:
        self.play_button = PlayButton(
            self,
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 + 40,
            width=160,
            height=60,
            font_color=arcade.color.BLACK
        )
        self.window.button_list.append(self.play_button)

        self.leaderboard_button = LeaderboardButton(
            self,
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 - 40,
            width=160,
            height=60,
            font_color=arcade.color.BLACK
        )
        self.window.button_list.append(self.leaderboard_button)

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

        self.play_button.draw()
        self.leaderboard_button.draw()
        self.game_title.draw()
