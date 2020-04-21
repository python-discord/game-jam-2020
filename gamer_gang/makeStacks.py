from PIL import Image
from itertools import permutations

players = [Image.open('images/mobs/player/1.png'), Image.open('images/mobs/player/2.png'), Image.open(
    'images/mobs/player/3.png')]

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

for part in permutations(players, 2):
    top = players.index(part[0]) + 1
    bottom = players.index(part[1]) + 1
    get_concat_v(part[0], part[1]).save(f'images/mobs/player/{top}on{bottom}.png')

for part in permutations(players):
    top = players.index(part[0]) + 1
    middle = players.index(part[1]) + 1
    bottom = players.index(part[2]) + 1
    get_concat_v(part[0], part[1]).save(f'images/mobs/player/{top}on{middle}.png')
    second = Image.open(f'images/mobs/player/{top}on{middle}.png')
    get_concat_v(second, part[2]).save(f'images/mobs/player/{top}on{middle}on{bottom}.png')
