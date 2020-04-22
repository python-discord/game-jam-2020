import random
from collections import namedtuple
from pathlib import Path
from typing import List, NamedTuple


class RowItem(NamedTuple):
    """
    A simple object to hold the filepath of an object, and the identifier for that object.
    For example, the title of an object might be Dracula or Plum, which can be used in clue creation,
    and the filepath will be the complete filepath.

    Attributes can be accessed with row_item_instance.title/row_item_instance.file_path
    """
    title: str
    file_path: str


def get_row_attrs(row_num: int, count: int = 3) -> List[RowItem]:
    """
    :param row_num: the row to be retrieved, either 1, 2, or 3
    :param count: the amount of items to be returned
    :return: a named tuple object with a title and a full file path
    """
    asset_path = Path(f'assets\\row_{row_num}')
    all_files = asset_path.rglob('*.png')
    all_row_items = [RowItem(file.name[:-4], str(file)) for file in all_files]
    row_items = random.sample(all_row_items, count)
    return row_items


def get_new_game():
    solution_list = get_row_attrs(1) + get_row_attrs(2) + get_row_attrs(3)
    return solution_list


def get_puzzle_clues(solution_list, fact_templates):
    # example_fact_template =
    #     ["{0} live next to the person who likes {4}",
    #      "The person in the {8} house likes {5}",
    #      "The person who likes {4} lives in the {7} house",
    #      "The person who likes {3} doesn't live next to the person who likes {5}",
    #      "{2}'s house is {8}",
    #      "{0} lives to the left of the {8} house."]
    # example_solution =
    #     ['Tom','Dick','Harry','Grapes','Cherries','Blueberries','Red',
    #      'White','Blue']
    # should result in
    #
    # ["Tom live next to the person who likes cherries",
    #  "The person in the blue house likes blueberries",
    #  "The person who likes cherries lives in the white house",
    #  "The person who likes grapes doesn't live next to the person who likes bluberries",
    #  "Harry's house is blue"]
    #
    #
    # apply solution_list elements to fact_templates
    # clue_list = applied solution_list to fact_templates
    return clue_list


def get_fact_template():
    # need some storage for these and choose one group at random
    # instead of a list of 9 Nones :)
    template_list = [None] * 9
    return template_list


def check_results(result, solution_list):
    return result == solution_list


def start_new_game():
    solution_list = get_new_game()
    shuffled_list = solution_list[:]
    random.shuffle(shuffled_list)
    fact_templates = get_fact_template()
    clue_list = get_puzzle_clues(solution_list, fact_templates)
    # real return value
    # return solution_list, shuffled_list, clue_list

    # bogus test code follows:
    solution_list = ['Tom', 'Dick', 'Harry', 'Grapes', 'Cherries', 'Blueberries', 'Red', 'White', 'Blue']
    clue_list = ["Tom live next to the person who likes cherries",
                 "The person in the blue house likes blueberries",
                 "The person who likes cherries lives in the white house",
                 "The person who likes grapes doesn't live next to the person who likes bluberries",
                 "Harry's house is blue"]
    shuffled_list = solution_list[:]
    random.shuffle(shuffled_list)

    return solution_list, shuffled_list, clue_list
