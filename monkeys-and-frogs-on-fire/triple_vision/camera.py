import arcade

from triple_vision.constants import WINDOW_SIZE


class Camera:

    def __init__(
        self,
        view,
        viewport_left_margin,
        viewport_bottom_margin
    ) -> None:
        self.view = view
        self.player_sprite = view.player

        self.viewport_left_margin = viewport_left_margin
        self.viewport_bottom_margin = viewport_bottom_margin

        self.viewport_left = 0
        self.viewport_bottom = 0

    def update(self):
        changed = False

        # Scroll left
        left_boundary = self.viewport_left + self.viewport_left_margin
        if self.player_sprite.left < left_boundary:
            self.viewport_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.viewport_left + WINDOW_SIZE[0] - self.viewport_left_margin
        if self.player_sprite.right > right_boundary:
            self.viewport_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.viewport_bottom + WINDOW_SIZE[1] - self.viewport_bottom_margin
        if self.player_sprite.top > top_boundary:
            self.viewport_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.viewport_bottom + self.viewport_bottom_margin
        if self.player_sprite.bottom < bottom_boundary:
            self.viewport_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(
                self.viewport_left,
                WINDOW_SIZE[0] + self.viewport_left,
                self.viewport_bottom,
                WINDOW_SIZE[1] + self.viewport_bottom,
            )
