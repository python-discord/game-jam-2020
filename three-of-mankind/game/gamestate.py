class GameState:
    """Represent the state of the current game, and manage it."""

    def __init__(self):
        self.player = ...

    def on_update(self, delta_time: float) -> None:
        """Handle update event."""
        ...

    def on_draw(self) -> None:
        """Handle draw event."""
        ...
