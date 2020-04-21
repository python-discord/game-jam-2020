"""
tests.py
A file dedicated to testing our game and ensuring it can run.
Integrate this into your IDE's workflow to ensure the game runs from top to bottom.
The tests used here should test all of our game's features as best they can.
"""

import pytest

from typing import Pattern, List


class TestGame:
    """
    Tests that the Arcade framework runs the game correctly.
    Only tests that it launches and runs for a little bit, not that it is functioning properly.
    """

    def test_game_runs(self) -> None:
        """
        Simply test that the Game runs.
        """

        # imports
        from main import Game

        # instantiate and setup
        game = Game()
        game.setup()
        game.minimize()  # Minimizes window, should reduce annoyance a little bit.
        # test for 100 frames
        game.test(20)


class TestSprites:
    """
    Tests the Sprite classes as well as the available sprites.
    """

    @pytest.fixture
    def sprites(self) -> List[str]:
        """
        :return: List of absolute paths to Sprite images
        """

        import os
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        IMAGE_DIR = os.path.join(BASE_DIR, 'resources', 'images')

        _sprites = []
        for primary in os.listdir(IMAGE_DIR):
            for secondary in os.listdir(os.path.join(IMAGE_DIR, primary)):
                secondary = os.path.join(IMAGE_DIR, primary, secondary)
                if os.path.isfile(secondary):
                    _sprites.append(secondary)
                else:
                    _sprites.extend(
                        os.path.join(secondary, file) for file in
                        os.listdir(os.path.join(IMAGE_DIR, primary, secondary)))
        return _sprites

    @pytest.fixture
    def patterns(self) -> List[Pattern]:
        """
        :return: A list of Pattern objects to test.
        """
        import re
        _patterns = [
            r'\w+_(?:\w+_)?\d+\.(?:jp(?:eg|e|g)|png)',
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
            head, tail = os.path.split(sprite)
            if any(pattern.match(tail) is not None for pattern in patterns):
                continue
            pytest.fail(f"Sprite '{tail}' in '{head}' did not match the schema.")

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

    @pytest.fixture
    def levels(self) -> List[str]:
        """
        :return: List of paths to Level files
        """
        import os

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        LEVEL_DIR = os.path.join(BASE_DIR, 'resources', 'levels')
        levels = [os.path.join(LEVEL_DIR, file) for file in os.listdir(LEVEL_DIR)]

        return levels

    def test_levels_are_loadable(self, levels) -> None:
        """
        Tests whether or not a level can be loaded.
        """
        from map import Level

        for level in levels:
            Level.load_file(2, 3, level)


class TestDungeon:
    """
    Tests the Dungeon class.
    """


class TestMisc:
    """
    Tests things that don't fit anywhere else.
    """
