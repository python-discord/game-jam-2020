"""Read and write data to/from a JSON file."""
import json


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


def get_hiscore() -> int:
    """Get the current highest score."""
    scores = open_file().get('scores', [])
    if scores:
        return max(scores)
    return 0


def get_scores() -> list:
    """Get a list of all scores."""
    return open_file().get('scores', [])


def add_score(score: int):
    """Record a score."""
    data = open_file()
    if 'scores' in data:
        data['scores'].append(score)
    else:
        data['scores'] = [score]
    save_file(data)


def get_seconds() -> float:
    """Find out how many seconds the user has played for."""
    return open_file().get('seconds', 0)


def add_time(seconds: float):
    """Add the time, in seconds, a user played a game for."""
    data = open_file()
    if 'seconds' in data:
        data['seconds'] += seconds
    else:
        data['seconds'] = seconds
    save_file(data)
