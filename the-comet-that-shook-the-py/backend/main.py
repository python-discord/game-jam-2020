import random


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
