"""
tests.py
A file dedicated to testing our game and ensuring it can run.
Integrate this into your IDE's workflow to ensure the game runs from top to bottom.
The tests used here should test all of our game's features as best they can.
"""

import pytest


class TestGame:
    """
    Tests that the Arcade framework runs the game correctly.
    Only tests that it launches and runs for a little bit, not that it is functioning properly.
    """

    def test_game_runs(self):
        """
        Simply test that the Game runs.
        """

        # imports
        from main import Game

        # instantiate and setup
        game = Game()
        game.setup()
        # test for 100 frames
        game.test(100)


class TestSprites:
    """
    Tests the Sprite classes as well as the available sprites.
    """
    pass


class TestLevels:
    """
    Tests the Level class.
    """

    def loadble_level():
        pass


class TestDungeon:
    """
    Tests the Dungeon class.
    """


class TestMisc:
    """
    Tests things that don't fit anywhere else.
    """
