import arcade

from .game import AdventuresGame
from .constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH

AdventuresGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE).setup()
arcade.run()
