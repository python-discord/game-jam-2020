from typing import Optional, Tuple

import arcade


class TextInput:

    def __init__(
        self,
        center_x: float,
        center_y: float,
        width: float,
        height: float,
        box_color: Tuple[int, int, int, int] = arcade.color.WHITE,
        border_color: Tuple[int, int, int, int] = arcade.color.BLACK,
        border_width: float = 1,
        text: Optional[str] = None,
        text_color: Tuple[int, int, int, int] = arcade.color.BLACK,
        bold: bool = False,
        italic: bool = False,
        font_size: float = 12,
        horizontal_margin: float = 5,
        vertical_margin: float = 5,
        cursor_color: Tuple[int, int, int, int] = arcade.color.BLACK
    ) -> None:
        self.center_x = center_x
        self.center_y = center_y

        self.width = width
        self.height = height

        self.box_color = box_color
        self.border_color = border_color
        self.border_width = border_width

        self.text = text
        self.text_color = text_color
        self.bold = bold
        self.italic = italic
        self.font_size = font_size

        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin

        self.shapes = arcade.ShapeElementList()
        self.shapes.append(
            arcade.create_rectangle_filled(
                center_x=center_x,
                center_y=center_y,
                width=width,
                height=height,
                color=box_color
            ),
        )
        self.shapes.append(
            arcade.create_rectangle_outline(
                center_x=center_x,
                center_y=center_y,
                width=width,
                height=height,
                color=border_color,
                border_width=border_width
            )
        )

        self.text_sprites = arcade.SpriteList()

        text_sprite = arcade.draw_text(
            text=text or 'L',
            start_x=center_x - (width / 2) + horizontal_margin,
            start_y=center_y - (height / 2) + vertical_margin,
            color=text_color,
            font_size=font_size,
            bold=bold,
            italic=italic
        )
        if not text:
            text_sprite.alpha = 0

        self.text_sprites.append(text_sprite)

        self.cursor_sprites = arcade.ShapeElementList()
        self.cursor = arcade.create_rectangle_filled(
            center_x=center_x - (width / 2) + horizontal_margin,
            center_y=center_y - (height / 2) + vertical_margin + text_sprite.height / 2,
            width=1,
            height=text_sprite.height,
            color=cursor_color
        )
        self.cursor_sprites.append(self.cursor)

        self.cursor_color = cursor_color
        self.cursor_idx = 0

        self.cursor_is_active = True
        self.cursor_blink_delta = 0

    def draw(self) -> None:
        self.shapes.draw()
        self.text_sprites.draw()
        self.cursor_sprites.draw()

    def on_update(self, delta_time: float = 1/60) -> None:
        self.cursor_blink_delta += delta_time

        if self.cursor_blink_delta > 0.5:
            self.cursor_sprites.remove(self.cursor)

            center_x = self.center_x - (self.width / 2) + self.horizontal_margin
            center_y = self.center_y - (self.height / 2) + self.vertical_margin + self.text_sprites[0].height / 2

            if self.cursor_is_active:
                self.cursor = arcade.create_rectangle_filled(
                    center_x=center_x,
                    center_y=center_y,
                    width=1,
                    height=self.text_sprites[0].height,
                    color=self.box_color
                )
                self.cursor_sprites.append(self.cursor)
                self.cursor_is_active = False

            else:
                self.cursor = arcade.create_rectangle_filled(
                    center_x=center_x,
                    center_y=center_y,
                    width=1,
                    height=self.text_sprites[0].height,
                    color=self.cursor_color
                )
                self.cursor_sprites.append(self.cursor)
                self.cursor_is_active = True

            self.cursor_blink_delta = 0


if __name__ == "__main__":
    WINDOW_SIZE = (1280, 720)

    class Test(arcade.Window):

        def __init__(self) -> None:
            super().__init__(*WINDOW_SIZE, 'Test Window')
            self.text_input = None

            arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        def setup(self) -> None:
            self.text_input = TextInput(
                WINDOW_SIZE[0] / 2,
                WINDOW_SIZE[1] / 2,
                300, 25
            )

        def on_draw(self) -> None:
            arcade.start_render()
            self.text_input.draw()

        def on_update(self, delta_time: float = 1/60) -> None:
            self.text_input.on_update(delta_time)

    test = Test()
    test.setup()

    arcade.run()
