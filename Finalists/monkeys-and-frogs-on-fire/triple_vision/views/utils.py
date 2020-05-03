from typing import Any, Tuple

import arcade


class BackButton(arcade.Sprite):
    """Replaces arcade.TextButton to deal with viewport"""

    def __init__(
        self,
        view: arcade.View,
        clicked: str,
        normal: str,
        viewport: Tuple[float, float],
        *args: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(filename=normal, *args, **kwargs)

        self.view = view

        self.clicked = arcade.load_texture(clicked)
        self.normal = arcade.load_texture(normal)

        self.viewport = viewport

        self.pressed = False

    def check_mouse_press(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                self.center_x - self.viewport[0] - self.width / 2 < x <
                self.center_x - self.viewport[0] + self.width / 2 and
                self.center_y - self.viewport[1] - self.width / 2 < y <
                self.center_y - self.viewport[1] + self.width / 2
            ):
                self.texture = self.clicked
                self.pressed = True

    def check_mouse_release(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                self.center_x - self.viewport[0] - self.width / 2 < x <
                self.center_x - self.viewport[0] + self.width / 2 and
                self.center_y - self.viewport[1] - self.width / 2 < y <
                self.center_y - self.viewport[1] + self.width / 2
            ):
                self.view.back()
                self.texture = self.normal
                self.pressed = False
