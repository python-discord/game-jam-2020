import logging

import arcade
from .gamestate import GameState
from .effects import ColorIsolationWindow

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "lemon is epic"

format_string = "%(asctime)s | %(filename)s#%(lineno)d | %(levelname)s | %(message)s"
logging.basicConfig(format=format_string, level=logging.DEBUG)


class Game(ColorIsolationWindow):
    """Main game object."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ingame = False
        self.gamestate = None
        self.set_isolation_color((49, 119, 255))

    def on_update(self, delta_time: float) -> None:
        """Send update event to the gamestate."""
        if not self.ingame:  # Temporarily automatically start the game if it isn't running
            self.start_game()
        if self.gamestate:
            self.gamestate.on_update(delta_time)

    def render(self) -> None:
        """Send draw event to the gamestate."""
        if self.gamestate:
            self.gamestate.on_draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """Send keypress event to the gamestate."""
        if self.gamestate:
            self.gamestate.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        """Send keyrelease event to the gamestate."""
        if self.gamestate:
            self.gamestate.on_key_release(symbol, modifiers)

    def start_game(self) -> None:
        """Create gamestate and set to the ingame mode."""
        logging.info('New game started')
        self.ingame = True
        self.gamestate = GameState()


# Start game
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
arcade.set_background_color((20, 20, 20))
arcade.run()
