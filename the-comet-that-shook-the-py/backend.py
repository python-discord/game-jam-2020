"""Backend API module."""


import random
import os
from pathlib import Path
from typing import List


def _get_count_files_starting_with(prefix: str, count=3) -> List[str]:
    """Retrieve 'count' random files starting with the given prefix.

    :param prefix: the prefix to use to retrieve assets
    :return: a list of the relative filenames
    """
    asset_path = Path('assets')
    all_files = asset_path.rglob(f'{prefix}_*')
    all_row_items = [file.name for file in all_files]
    return random.sample(all_row_items, count)


def _get_r1_attrs(count=3) -> List[str]:
    """Retrive 'count' randomized first row attributes."""
    attrs = _get_count_files_starting_with("R1", count)
    return attrs


def _get_r2_attrs(count=3) -> List[str]:
    """Retrive 'count' randomized second row attributes."""
    attrs = _get_count_files_starting_with("R2", count)
    return attrs


def _get_r3_attrs(count=3) -> List[str]:
    """Retrive 'count' randomized third row attributes."""
    attrs = _get_count_files_starting_with("R3", count)
    return attrs


def _get_fact_template(filename=None, count=1) -> List[str]:
    """Retrive 'count' randomized clue template.

    The count should always be 1.
    """
    if not filename:
        filename = _get_count_files_starting_with('f1', count)

    filename = os.path.join('assets', filename[0])
    with open(filename, 'rt', encoding='utf8') as file:
        template = file.read().rstrip().splitlines()

    return template


def _get_new_game():
    """Build a new solution in order to create a new game."""
    solution_list = _get_r1_attrs() + _get_r2_attrs() + _get_r3_attrs()
    return solution_list


def _get_puzzle_clues(solution_list, fact_template):
    """Build a working set of clues from a template and a given solution."""
    if not solution_list or not fact_template:
        raise TypeError("Missing input for function get_puzzle_clues!")

    return [fact.format(*[item.split('_')[1] for item in solution_list])
            for fact in fact_template]


def check_results(result, solution_list):
    """Compare a working solution to an attempted solution."""
    return result == solution_list


def start_new_game():
    """Create and return a new game.

    Includes the solution, shuffled list of assets, and clues."""
    solution_list = _get_new_game()
    shuffled_list = solution_list[:]
    random.shuffle(shuffled_list)
    fact_template = _get_fact_template()
    clue_list = _get_puzzle_clues(solution_list, fact_template)

    return solution_list, shuffled_list, clue_list, fact_template


if __name__ == '__main__':
    A, B, C, D = start_new_game()

    print("\n-=*Solution*=-")
    for i, v in enumerate(A):
        print(f'{i}: {v}')

    print("\n-=*Shuffled Assets*=-")
    for i, v in enumerate(B):
        print(f'{i}: {v}')

    print("\n-=*Clues*=-")
    for i, v in enumerate(C):
        print(f'{i}: {v}')

    print("\n-=*Empty Template*=-")
    for i, v in enumerate(D):
        print(f'{i}: {v}')
