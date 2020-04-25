"""Read and write data to/from a JSON file."""
import json
import typing

from constants import AWARDS


FILE = 'data/scores.json'


def open_file() -> dict:
    """Open the file, if present, if not, return an empty dict."""
    try:
        with open(FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_file(data: dict):
    """Save the file with modified data."""
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=1)


def data_util(fun: typing.Callable) -> typing.Callable:
    """Wrap functions that need read/write access to the data."""
    def wrapper(*args, **kwargs) -> typing.Any:
        """Open the file and save it again."""
        data = open_file()
        ret = fun(data, *args, **kwargs)
        save_file(data)
        return ret

    return wrapper


@data_util
def get_hiscore(data: dict) -> int:
    """Get the current highest score."""
    scores = data.get('scores', [])
    if scores:
        return max(scores)
    return 0


@data_util
def get_scores(data: dict) -> list:
    """Get a list of all scores."""
    return data.get('scores', [])


@data_util
def add_score(data: dict, score: int):
    """Record a score."""
    if 'scores' in data:
        data['scores'].append(score)
    else:
        data['scores'] = [score]


@data_util
def get_seconds(data: dict) -> float:
    """Find out how many seconds the user has played for."""
    return data.get('seconds', 0)


@data_util
def add_time(data: dict, seconds: float):
    """Add the time, in seconds, a user played a game for."""
    if 'seconds' in data:
        data['seconds'] += seconds
    else:
        data['seconds'] = seconds


@data_util
def get_awards(data: dict) -> list:
    """Find out what awards the user has."""
    award_nums = data.get('awards', [])
    awards = []
    for num, award in enumerate(AWARDS):
        copy: typing.Dict[str, typing.Any] = dict(award)
        copy['achieved'] = num in award_nums
        awards.append(copy)
    return awards


@data_util
def add_award(data: dict, number: int):
    """Add an award if it has not already been achieved."""
    if 'awards' in data:
        if number not in data:
            data['awards'].append(number)
    else:
        data['awards'] = [number]
