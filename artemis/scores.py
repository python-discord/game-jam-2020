import json


FILE = 'data/scores.json'


def open_file():
    try:
        with open(FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_file(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=1)


def get_hiscore():
    scores = open_file().get('scores', [])
    if scores:
        return max(scores)
    return 0


def get_scores():
    return open_file().get('scores', [])


def add_score(score):
    data = open_file()
    if 'scores' in data:
        data['scores'].append(score)
    else:
        data['scores'] = [score]
    save_file(data)


def get_seconds():
    return open_file().get('seconds', 0)


def add_time(seconds):
    data = open_file()
    if 'seconds' in data:
        data['seconds'] += seconds
    else:
        data['seconds'] = seconds
    save_file(data)
