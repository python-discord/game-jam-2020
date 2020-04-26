from datetime import datetime
from typing import Tuple

import arcade
from frost.client.objects import Memory

from triple_vision import Settings as s
from triple_vision.networking import client, get_status
from triple_vision.views.utils import BackButton


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

        self._center_x = center_x
        self._center_y = center_y

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

        self.elements = arcade.ShapeElementList()
        self.elements.append(self.display)
        self.elements.append(self.display_outline)

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

    @property
    def center_x(self) -> float:
        return self._center_x

    @center_x.setter
    def center_x(self, value: float) -> None:
        self.elements.center_x = value
        self.username_text.center_x = value
        self.score_text.center_x = value
        self.timestamp_text.center_x = value
        self._center_x = value

    @property
    def center_y(self) -> float:
        return self._center_y

    @center_y.setter
    def center_y(self, value: float) -> None:
        self.elements.center_y = value
        self.username_text.center_y = value
        self.score_text.center_y = value
        self.timestamp_text.center_y = value
        self._center_y = value

    def draw(self) -> None:
        self.elements.draw()

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

        self.viewport = [0, 0]
        self.prev_viewport = [0, 0]

        self.background = arcade.load_texture('assets/background.png')

    def back(self) -> None:
        self.window.button_list.clear()

        arcade.set_viewport(0, s.WINDOW_SIZE[0], 0, s.WINDOW_SIZE[1])

        self.window.show_view(self.main_view)

    def on_show(self) -> None:
        self.back_button = BackButton(
            self,
            clicked='assets/buttons/back_pressed.png',
            normal='assets/buttons/back_released.png',
            center_x=60,
            center_y=30,
            viewport=self.viewport
        )
        self.window.button_list.append(self.back_button)

        self.game_title = arcade.load_texture(
            'assets/title.png'
        )

        client.get_top_scores()
        get_status('get_top_scores')

        self.scores = Memory.scores

        for idx, score in enumerate(reversed(self.scores), -1):
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

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        self.back_button.check_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        self.back_button.check_mouse_release(x, y, button, modifiers)

    def on_draw(self) -> None:
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(
            *self.viewport,
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

        for node in self.score_nodes:
            node.draw()

        self.back_button.draw()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        self.viewport[1] += scroll_y * 10

        arcade.set_viewport(
            self.viewport[0],
            self.viewport[0] + s.WINDOW_SIZE[0],
            self.viewport[1],
            self.viewport[1] + s.WINDOW_SIZE[1]
        )

        delta_viewport = (
            self.viewport[0] - self.prev_viewport[0],
            self.viewport[1] - self.prev_viewport[1]
        )

        self.back_button.center_x += delta_viewport[0]
        self.back_button.center_y += delta_viewport[1]

        for node in self.score_nodes:
            node.elements.center_x -= delta_viewport[0]
            node.elements.center_y -= delta_viewport[1]

        self.prev_viewport = self.viewport.copy()
