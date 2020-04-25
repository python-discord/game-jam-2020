from datetime import datetime
from typing import Tuple

import arcade

from frost.client.objects import Memory

from triple_vision import Settings as s
from triple_vision.networking import client, get_status


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


class ScoreNode:

    def __init__(
        self,
        username: str,
        score: int,
        timestamp: str,
        center_x: float,
        center_y: float,
        width: float,
        height: float,
        text_color: Tuple[int, int, int, int] = arcade.color.BLACK,
        display_color: Tuple[int, int, int, int] = arcade.color.WHITE,
        outline_color: Tuple[int, int, int, int] = arcade.color.BLACK,
        outline_width: float = 1
    ) -> None:
        self.username = username
        self.score = score
        self.timestamp = datetime.fromisoformat(timestamp).strftime(r'%d/%m/%Y | %I:%M %p')

        self.center_x = center_x
        self.center_y = center_y

        self.width = width
        self.height = height

        self.text_color = text_color
        self.display_color = display_color
        self.outline_color = outline_color
        self.outline_width = outline_width

        self.display = arcade.create_rectangle_filled(
            center_x=center_x,
            center_y=center_y,
            width=width,
            height=height,
            color=display_color
        )

        self.display_outline = arcade.create_rectangle_outline(
            center_x=center_x,
            center_y=center_y,
            width=width,
            height=height,
            color=outline_color,
            border_width=outline_width
        )

        self.username_text = arcade.draw_text(
            text=username,
            start_x=center_x - width / 2 + 20,
            start_y=center_y,
            color=text_color,
            anchor_y='center'
        )

        self.score_text = arcade.draw_text(
            text=str(score),
            start_x=center_x,
            start_y=center_y,
            color=text_color,
            anchor_y='center'
        )

        self.timestamp_text = arcade.draw_text(
            text=self.timestamp,
            start_x=center_x + width / 2 - 200,
            start_y=center_y,
            color=text_color,
            anchor_y='center'
        )

        arcade.text.draw_text_cache.clear()

    def draw(self) -> None:
        self.display.draw()
        self.display_outline.draw()

        self.username_text.draw()
        self.score_text.draw()
        self.timestamp_text.draw()


class LeaderboardView(arcade.View):

    def __init__(self, main_view: arcade.View) -> None:
        super().__init__()

        self.main_view = main_view

        self.back_button = None
        self.game_title = None

        self.score_nodes = list()
        self.scores = None

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

        client.get_top_scores()
        get_status('get_top_scores')

        self.scores = Memory.scores

        for idx, score in enumerate(self.scores, -1):
            self.score_nodes.append(
                ScoreNode(
                    username=score['username'],
                    score=score['score'],
                    timestamp=score['timestamp'],
                    center_x=s.WINDOW_SIZE[0] / 2,
                    center_y=s.WINDOW_SIZE[1] - (len(self.scores) - idx) * 120,
                    width=s.WINDOW_SIZE[0] / 8 * 7,
                    height=100,
                    outline_width=3,
                    display_color=(240, 240, 240, 255)
                )
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

        for node in self.score_nodes:
            node.draw()
