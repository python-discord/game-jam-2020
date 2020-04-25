import arcade

from triple_vision import Settings as s
from triple_vision.triple_vision import TripleVision
from triple_vision.views.leaderboard_view import LeaderboardView


class PlayButton(arcade.TextButton):

    def __init__(self, view, *args, **kwargs) -> None:
        super().__init__(text='', *args, **kwargs)
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
        super().__init__(text='', *args, **kwargs)
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
        self.window.show_view(TripleVision(self))

    def leaderboard(self) -> None:
        self.window.button_list.clear()
        self.window.show_view(LeaderboardView(self))

    def on_show(self) -> None:
        play_button_theme = arcade.Theme()
        play_button_theme.add_button_textures(
            clicked='assets/buttons/play_pressed.png',
            normal='assets/buttons/play_released.png'
        )

        self.play_button = PlayButton(
            self,
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 + 50,
            width=150,
            height=80,
            theme=play_button_theme
        )
        self.window.button_list.append(self.play_button)

        leaderboard_button_theme = arcade.Theme()
        leaderboard_button_theme.add_button_textures(
            clicked='assets/buttons/leaderboard_pressed.png',
            normal='assets/buttons/leaderboard_released.png'
        )

        self.leaderboard_button = LeaderboardButton(
            self,
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 - 50,
            width=150,
            height=80,
            theme=leaderboard_button_theme
        )
        self.window.button_list.append(self.leaderboard_button)

        self.game_title = arcade.load_texture(
            'assets/title.png'
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

        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=s.WINDOW_SIZE[0] / 2 - 449,
            bottom_left_y=s.WINDOW_SIZE[1] / 8 * 7 - 200,
            width=898,
            height=400,
            texture=self.game_title
        )

        self.play_button.draw()
        self.leaderboard_button.draw()
