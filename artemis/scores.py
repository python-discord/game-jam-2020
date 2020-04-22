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


def add_score(score):
    data = open_file()
    if 'scores' in data:
        data['scores'].append(score)
    else:
        data['scores'] = [score]
    save_file(data)


def get_achievements():
    achievements = open_file().get('achievments', [])
    ordered = []
    