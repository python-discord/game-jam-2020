from typing import Tuple

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

        self.text = ''
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
        self.text_sprites.append(
            arcade.draw_text(
                text='',
                start_x=center_x - (width / 2) + horizontal_margin,
                start_y=center_y - (height / 2) + vertical_margin,
                color=text_color,
                font_size=font_size,
                bold=bold,
                italic=italic
            )
        )

        self.cursor_sprites = arcade.ShapeElementList()
        self.cursor = arcade.create_rectangle_filled(
            center_x=center_x - (width / 2) + horizontal_margin,
            center_y=center_y - (height / 2) + vertical_margin + self.text_sprites[0].height / 2,
            width=1,
            height=self.text_sprites[0].height,
            color=self.box_color
        )
        self.cursor_sprites.append(self.cursor)

        self.cursor_color = cursor_color
        self.prev_cursor_idx = 0
        self.cursor_idx = 0

        self.cursor_is_active = True
        self.cursor_blink_delta = 0

        self._active = True

    @property
    def cursor_pos(self) -> Tuple[float, float]:
        center_x = self.center_x - (self.width / 2) + self.horizontal_margin + \
                sum(text_sprite.width for text_sprite in self.text_sprites[:self.cursor_idx]) + 1

        center_y = self.center_y - (self.height / 2) + self.vertical_margin + \
            self.text_sprites[0].height / 2

        return center_x, center_y

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        if not value:
            self.cursor_sprites.remove(self.cursor)

            self.cursor = arcade.create_rectangle_filled(
                *self.cursor_pos,
                width=1,
                height=self.text_sprites[0].height,
                color=self.box_color
            )
            self.cursor_sprites.append(self.cursor)

        self._active = value

    def draw_cursor(self, center_x: float, center_y: float, color: Tuple[int, int, int, int]) -> None:
        self.cursor_sprites.remove(self.cursor)

        self.cursor = arcade.create_rectangle_filled(
            center_x=center_x,
            center_y=center_y,
            width=1,
            height=self.text_sprites[self.cursor_idx].height,
            color=color
        )

        self.cursor_sprites.append(self.cursor)

    def draw_text_at_cursor(self, text: str) -> None:
        start_x = self.center_x - (self.width / 2) + self.horizontal_margin + \
            sum(text_sprite.width for text_sprite in self.text_sprites[:self.cursor_idx])

        start_y = self.center_y - (self.height / 2) + self.vertical_margin

        text_sprite = arcade.draw_text(
            text=text,
            start_x=start_x,
            start_y=start_y,
            color=self.text_color,
            font_size=self.font_size,
            bold=self.bold,
            italic=self.italic
        )

        if (
            sum(sprite.width for sprite in self.text_sprites) + text_sprite.width >
            self.width - self.horizontal_margin * 2
        ):
            return

        self.text = self.text[:self.cursor_idx] + text + self.text[self.cursor_idx:]

        for sprite in self.text_sprites[self.cursor_idx:]:
            sprite.center_x += text_sprite.width

        self.text_sprites.insert(self.cursor_idx, text_sprite)
        self.cursor_idx += 1

        # Prevent the use of the same instance
        arcade.text.draw_text_cache.clear()

    def delete_text(self, idx) -> None:
        self.text = self.text[:idx] + self.text[idx + 1:]
        old_sprite = self.text_sprites.pop(idx)

        for sprite in self.text_sprites[idx:]:
            sprite.center_x -= old_sprite.width

    def move_cursor(self) -> bool:
        if self.prev_cursor_idx != self.cursor_idx:
            self.draw_cursor(*self.cursor_pos, self.cursor_color)
            self.prev_cursor_idx = self.cursor_idx

            return True

        return False

    def process_mouse_press(self, x, y, button, modifiers) -> None:
        if (
            self.center_x - self.width / 2 < x < self.center_x + self.width / 2 and
            self.center_y - self.height / 2 < y < self.center_y + self.height / 2
        ):
            for idx, text_sprite in enumerate(self.text_sprites):
                if text_sprite.left <= x <= text_sprite.right:
                    self.cursor_idx = idx
                    break

            self.active = True

        else:
            self.active = False

    def process_key_press(self, key, modifiers) -> None:
        if not self.active:
            return

        if 32 <= key <= 126:
            if modifiers & 1 == arcade.key.MOD_SHIFT:
                key -= 32

            self.draw_text_at_cursor(chr(key))

        elif key == arcade.key.BACKSPACE:
            if len(self.text) > 0:
                self.delete_text(self.cursor_idx - 1)
                self.cursor_idx -= 1

        elif key == arcade.key.DELETE:

            if self.cursor_idx < len(self.text):
                self.delete_text(self.cursor_idx)

        elif key == arcade.key.LEFT:
            if self.cursor_idx > 0:
                self.cursor_idx -= 1

        elif key == arcade.key.RIGHT:
            if self.cursor_idx < len(self.text):
                self.cursor_idx += 1

        elif key == arcade.key.ENTER:
            self.on_enter(self.text)

    def on_enter(self, text) -> None:
        pass

    def draw(self) -> None:
        self.shapes.draw()
        self.text_sprites.draw()
        self.cursor_sprites.draw()

    def on_update(self, delta_time: float = 1/60) -> None:
        if not self.active:
            return

        if self.move_cursor():
            return

        self.cursor_blink_delta += delta_time

        if self.cursor_blink_delta > 0.5:

            if self.cursor_is_active:
                color = self.box_color
                self.cursor_is_active = False

            else:
                color = self.cursor_color
                self.cursor_is_active = True

            self.draw_cursor(*self.cursor_pos, color)
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

        def on_mouse_press(self, x, y, button, modifiers) -> None:
            self.text_input.process_mouse_press(x, y, button, modifiers)

        def on_key_press(self, key, modifiers) -> None:
            self.text_input.process_key_press(key, modifiers)

        def on_draw(self) -> None:
            arcade.start_render()
            self.text_input.draw()

        def on_update(self, delta_time: float = 1/60) -> None:
            self.text_input.on_update(delta_time)

    test = Test()
    test.setup()

    arcade.run()
