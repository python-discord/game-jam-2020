from .player import Player
import arcade

FLOOR_LENGTH = 60
FLOOR_TEXTURE_LENGTH = 100


class GameState:
    """Represent the state of the current game, and manage it."""

    def __init__(self):
        self.level_geometry = arcade.SpriteList()

        self.player = Player('assets/placeholders/player.png')
        self.player.center_x = 200
        self.player.center_y = 200

        for left in range(0, FLOOR_LENGTH * FLOOR_TEXTURE_LENGTH, FLOOR_TEXTURE_LENGTH):
            floor = arcade.Sprite('assets/placeholders/floor.png')
            floor.left = left
            floor.bottom = 0
            self.level_geometry.append(floor)

    def on_update(self, delta_time: float) -> None:
        """Handle update event."""
        ...

    def on_draw(self) -> None:
        """Handle draw event."""
        self.player.draw()
        self.level_geometry.draw()
