import arcade


class Camera:
    def __init__(
        self,
        player_sprite,
        window_height,
        window_width,
        viewport_left,
        viewport_bottom,
        viewport_margin,
    ):
        """viewport is a tuple of coordinates (x, y)"""
        self.player_sprite = player_sprite
        self.window_height = window_height
        self.window_width = window_width
        self.margin = viewport_margin
        self.viewport_left, self.viewport_bottom = viewport_left, viewport_bottom

    def update(self):
        changed = False

        # Scroll left
        left_boundary = self.viewport_left + self.margin
        if self.player_sprite.left < left_boundary:
            self.viewport_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.viewport_left + self.window_width - self.margin
        if self.player_sprite.right > right_boundary:
            self.viewport_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.viewport_bottom + self.window_width - self.margin
        if self.player_sprite.top > top_boundary:
            self.viewport_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.viewport_bottom + self.margin
        if self.player_sprite.bottom < bottom_boundary:
            self.viewport_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(
                self.viewport_left,
                self.window_width + self.viewport_left,
                self.viewport_bottom,
                self.window_height + self.viewport_bottom,
            )
