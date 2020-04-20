from PIL import Image
from itertools import permutations

players = [Image.open('images/player/player1.jpg'), Image.open('images/player/player2.jpg'), Image.open('images/player/player3.jpg')]

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

for part in permutations(players, 2):
    top = players.index(part[0]) + 1
    bottom = players.index(part[1]) + 1
    get_concat_v(part[0], part[1]).save(f'images/player/{top}on{bottom}.jpg')

for part in permutations(players):
    top = players.index(part[0]) + 1
    middle = players.index(part[1]) + 1
    bottom = players.index(part[2]) + 1
    get_concat_v(part[0], part[1]).save(f'images/player/{top}on{middle}.jpg')
    second = Image.open(f'images/player/{top}on{middle}.jpg')
    get_concat_v(second, part[2]).save(f'images/player/{top}on{middle}on{bottom}.jpg')
