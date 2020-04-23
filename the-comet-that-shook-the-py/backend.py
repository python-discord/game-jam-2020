import random
from pathlib import Path
from typing import List


def _get_count_files_starting_with(prefix: str) -> List[str]:
    """
    :param prefix: the prefix to use to retrieve assets
    :return: a list of the relative filenames
    """
    asset_path = Path('assets')
    all_files = asset_path.rglob(f'{prefix}_*')
    all_row_items = [file.name for file in all_files]
    return all_row_items


def get_r1_attrs(count=3) -> List[str]:
    attrs = _get_count_files_starting_with("R1")
    return random.sample(attrs, count)


def get_r2_attrs(count=3) -> List[str]:
    attrs = _get_count_files_starting_with("R2")
    return random.sample(attrs, count)


def get_r3_attrs(count=3) -> List[str]:
    attrs = _get_count_files_starting_with("R3")
    return random.sample(attrs, count)


def get_new_game():
    solution_list = get_r1_attrs() + get_r2_attrs() + get_r3_attrs()
    return solution_list


def get_puzzle_clues(solution_list, fact_templates):
    if not solution_list or not fact_templates:
        raise TypeError("Missing input for function get_puzzle_clues!")

    return [fact.format(*solution_list) for fact in fact_templates]


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
    # real return value
    # return solution_list, shuffled_list, clue_list
    clue_list = get_puzzle_clues(solution_list, fact_templates)

    return solution_list, shuffled_list, clue_list
