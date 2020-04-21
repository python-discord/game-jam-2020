"""
tests.py
A file dedicated to testing our game and ensuring it can run.
Integrate this into your IDE's workflow to ensure the game runs from top to bottom.
The tests used here should test all of our game's features as best they can.
"""
from typing import Pattern, List

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
        game.test(50)


class TestSprites:
    """
    Tests the Sprite classes as well as the available sprites.
    """

    @pytest.fixture
    def sprites(self) -> List[str]:
        """
        Returns a list of absolute paths to sprites found in the images folder.

        :return: List of absolute paths to sprites
        """

        import os
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGE_DIR = os.path.join(BASE_DIR, 'resources', 'images')

        _sprites = []
        for primary in os.listdir(IMAGE_DIR):
            for secondary in os.listdir(os.path.join(IMAGE_DIR, primary)):
                _sprites.extend(os.listdir(os.path.join(IMAGE_DIR, primary, secondary)))
        return _sprites

    @pytest.fixture
    def patterns(self) -> List[Pattern]:
        """
        Returns a list of RegEx
        :return: A list of Pattern objects
        """
        import re
        _patterns = [
            r'\w+_(?:\w+_)?\d+\.(?:jp(?:eg|e|g)|png)'
            r'\w+\d+\.(?:jp(?:eg|e|g)|png)',
            r'\w+_tile\.(?:jp(?:eg|e|g)|png)'
        ]
        return list(map(re.compile, _patterns))

    def test_sprite_schema(self, sprites: List[str], patterns: List[Pattern]) -> None:
        """
        Tests that all sprites follow the naming conventions.
        """
        import os

        for sprite in sprites:
            for pattern in patterns:
                if pattern.match(os.path.basename(sprite)):
                    continue
            pytest.fail(f"Sprite '{sprite}' did not match the schema.")

    def test_sprite_loads(self, sprites) -> None:
        """
        Tests that all sprites can be loaded by the arcade framework.
        """
        import arcade

        for sprite in sprites:
            _sprite = arcade.Sprite(sprite)


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
