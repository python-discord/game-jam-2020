import unittest
from backend import (
    _get_puzzle_clues,
    _get_fact_template,
)


class TestFactTemplate(unittest.TestCase):
    def testReturnTemplatesAsList(self):
        template_list = _get_fact_template()
        assert isinstance(template_list, list)

    def testReturnNonEmptyTemplatesList(self):
        template_list = _get_fact_template()
        assert len(template_list)

    def testTemplateListContainsListOfStrings(self):
        template_list = _get_fact_template()
        assert all([isinstance(x, str) for x in template_list])

    def testTemplateInnerListContainsStrings(self):
        template_list = _get_fact_template()
        assert isinstance(template_list[0][0], str)

    def testTemplateStringsAre9FormatStrings(self):
        template_list = _get_fact_template()
        FORMAT = ["TEST" for _ in range(10)]

        try:
            assert template_list[0].format(*FORMAT)
        except IndexError:
            assert False, "Failed test because of template mismatch"

    def testTemplateStringsFromFile(self):
        template_one_file = _get_fact_template(["f1_templates_001.temp"])
        assert template_one_file == [
            "{0} is next to the {4} programmer",
            "The person who uses {8} programs in {5}",
            "The {4} programmer uses {7}",
            "The {3} programmer isn't next to the {5} programmer",
            "{2} uses {8}",
        ]

    def testTemplateNoFile(self):
        self.assertRaises(FileNotFoundError, _get_fact_template,
                          "NotFoundFile.temp")

    def testNoEmptyStrings(self):
        template_list = _get_fact_template()
        assert all([len(clue) for file in template_list for clue in file])


class TestGetPuzzleClues(unittest.TestCase):
    def testNoneNone(self):
        self.assertRaises(TypeError, _get_puzzle_clues, None, None)

    def testNoneEmpty(self):
        self.assertRaises(TypeError, _get_puzzle_clues, None, [])

    def testEmptyNone(self):
        self.assertRaises(TypeError, _get_puzzle_clues, [], None)

    def testEmptyEmpty(self):
        self.assertRaises(TypeError, _get_puzzle_clues, [], [])

    def testLessSolutions(self):
        self.assertRaises(
            IndexError, _get_puzzle_clues, ["Microsoft"],
                                           ["{0} programmers use {1}"]
        )

    def testMoreSolutions(self):
        assert _get_puzzle_clues(
            ["pre_Microsoft_post", "pre_IBM_post", "pre_C#_post",
             "pre_python_post"],
            ["{0} programmers use {2}"],
        ) == ["Microsoft programmers use C#"]

    def testEqualSolutions(self):
        assert _get_puzzle_clues(
            ["pre_Microsoft_post", "pre_IBM_post", "pre_C#_post",
             "pre_python_post"],
            ["{0} programmers use {2}", "{1} programmers use {3}"],
        ) == ["Microsoft programmers use C#", "IBM programmers use python"]
