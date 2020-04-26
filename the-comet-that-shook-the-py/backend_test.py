"""Unit tests for backend API."""
import backend


def test_check_results_equal_true():
    assert(backend.check_results(['abc', 'def', 'ghi'], ['abc', 'def', 'ghi']))


def test_check_results_nequal_false():
    assert(not backend.check_results(['abc', 'def', 'ghi'],
                                     ['def', 'ghi', 'abc']))


def test_get_puzzle_clues():
    expected = ['abc foo def bar ghi', 'blah blah blah', 'def', 'ghi']
    actual = backend._get_puzzle_clues(
            ['pre_abc_000.ext', 'pre_def_000.ext', 'pre_ghi_000.ext'],
            ['{0} foo {1} bar {2}', 'blah blah blah', '{1}', '{2}'])
    assert(expected == actual)


def test_get_new_game():
    solution, shuffled, clues, template = backend.start_new_game()
    assert (backend.check_results(solution, solution))
    assert (not backend.check_results(solution, shuffled))
    assert (backend._get_puzzle_clues(solution, template) == clues)
