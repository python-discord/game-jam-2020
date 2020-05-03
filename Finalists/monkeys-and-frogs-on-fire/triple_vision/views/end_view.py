import arcade

from triple_vision import Settings as s


class GameOverView(arcade.View):

    def __init__(self, main_view, score) -> None:
        super().__init__()
        self.main_view = main_view
        self.score = score

        self.game_title = None
        self.game_over_text = None
        self.continue_text = None

        self.score_text = None

        self.background = None

    def on_show(self) -> None:
        self.game_title = arcade.load_texture('assets/title.png')

        self.game_over_text = arcade.load_texture('assets/game_over.png')
        self.continue_text = arcade.load_texture('assets/continue.png')

        self.background = arcade.load_texture('assets/background.png')

        self.score_text = arcade.draw_text(
            text=f'Score: {self.score}',
            start_x=s.WINDOW_SIZE[0] / 2,
            start_y=s.WINDOW_SIZE[1] / 2,
            color=arcade.color.WHITE,
            align='center',
            anchor_x='center',
            anchor_y='center',
            font_size=32
        )

    def on_draw(self) -> None:
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

        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=s.WINDOW_SIZE[0] / 2 - 449,
            bottom_left_y=s.WINDOW_SIZE[1] / 8 - 200,
            width=898,
            height=400,
            texture=self.continue_text
        )

        self.score_text.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.SPACE:
            self.window.show_view(self.main_view)
