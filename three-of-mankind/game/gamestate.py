from .player import Player


class GameState:
    """Represent the state of the current game, and manage it."""

    def __init__(self):
        self.player = Player('assets/placeholders/player.png')

    def on_update(self, delta_time: float) -> None:
        """Handle update event."""
        ...

    def on_draw(self) -> None:
        """Handle draw event."""
        self.player.draw()
