import unittest
from backend import get_puzzle_clues


class TestGetPuzzleClues(unittest.TestCase):

    def testNoneNone(self):
        self.assertRaises(TypeError, get_puzzle_clues, None, None)

    def testNoneEmpty(self):
        self.assertRaises(TypeError, get_puzzle_clues, None, None)

    def testEmptyNone(self):
        self.assertRaises(TypeError, get_puzzle_clues, None, None)

    def testEmptyEmpty(self):
        self.assertRaises(TypeError, get_puzzle_clues, None, None)

    def testLessSolutions(self):
        self.assertRaises(IndexError, get_puzzle_clues, ["Microsoft"], ["{0} programmers use {1}"])

    def testMoreSolutions(self):
        assert get_puzzle_clues(["Microsoft", "IBM", "C#", "python"], ["{0} programmers use {2}"]) == ["Microsoft programmers use C#"]

    def testEqualSolutions(self):
        assert get_puzzle_clues(["Microsoft", "IBM", "C#", "python"],
                                ["{0} programmers use {2}",
                                 "{1} programmers use {3}"]) == ["Microsoft programmers use C#",
                                                                   "IBM programmers use python"]
