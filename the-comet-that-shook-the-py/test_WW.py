import unittest
from backend import _get_count_files_starting_with, get_puzzle_clues, get_fact_templates


class TestFactTemplate(unittest.TestCase):

    def testReturnTemplatesAsList(self):
        template_list = get_fact_templates()
        assert isinstance(template_list, list)

    def testReturnNonEmptyTemplatesList(self):
        template_list = get_fact_templates()
        assert len(template_list)

    def testTemplateListContainsListOfLists(self):
        template_list = get_fact_templates()
        assert all([isinstance(x, list) for x in template_list])

    def testTemplateInnerListContainsStrings(self):
        template_list = get_fact_templates()
        assert isinstance(template_list[0][0], str)

    def testTemplateStringsAre9FormatStrings(self):
        template_list = get_fact_templates()
        FORMAT = ["TEST" for _ in range(10)]

        try:
            assert template_list[0][0].format(*FORMAT)
        except IndexError as e:
            assert False, "Failed test because of template mismatch"

    def testTemplateStringsFromFile(self):
        template_one_file = get_fact_templates(['f1_templates_001.temp', 'f1_templates_002.temp'])
        assert template_one_file == [['{0} is next to the {4} programmer', 'The person who uses {8} programs in {5}', 'The {4} programmer uses {7}', "The {3} programmer isn't next to the {5} programmer", '{2} uses {8}'], ['{1} is to the right of the {3} programmer', '{2} is to the right of the one who uses {6}', 'The {4} programmer does not use {6}', '{0} does not use {8}', "The person who uses {8} doesn't program in {4} ", "{2} doesn't program in {4}"]]

    def testTemplateNoFile(self):
        self.assertRaises(FileNotFoundError, get_fact_templates, 'NotFoundFile.temp')

    def testNoEmptyStrings(self):
        template_list = get_fact_templates()
        assert all([len(clue) for file in template_list for clue in file])

class TestGetPuzzleClues(unittest.TestCase):

    def testNoneNone(self):
        self.assertRaises(TypeError, get_puzzle_clues, None, None)

    def testNoneEmpty(self):
        self.assertRaises(TypeError, get_puzzle_clues, None, [])

    def testEmptyNone(self):
        self.assertRaises(TypeError, get_puzzle_clues, [], None)

    def testEmptyEmpty(self):
        self.assertRaises(TypeError, get_puzzle_clues, [], [])

    def testLessSolutions(self):
        self.assertRaises(IndexError, get_puzzle_clues, ["Microsoft"], ["{0} programmers use {1}"])

    def testMoreSolutions(self):
        assert get_puzzle_clues(["Microsoft", "IBM", "C#", "python"], ["{0} programmers use {2}"]) == [
            "Microsoft programmers use C#"]

    def testEqualSolutions(self):
        assert get_puzzle_clues(["Microsoft", "IBM", "C#", "python"],
                                ["{0} programmers use {2}",
                                 "{1} programmers use {3}"]) == ["Microsoft programmers use C#",
                                                                 "IBM programmers use python"]
