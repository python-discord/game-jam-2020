from PIL import Image
from itertools import permutations

players = ['1.png', '2.png', '3.png',
           'other1.png', 'other2.png', 'other3.png']

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

for part in permutations(players, 2):
    top = str(players.index(part[0]) + 1) if players.index(part[0]) <= 2 else 'other' + str(players.index(part[0]) - 2)
    down = str(players.index(part[1]) + 1) if players.index(part[1]) <= 2 else 'other' + str(players.index(part[1]) - 2)
    if int(top.replace('other', '')) == int(down.replace('other', '')):
        continue

    get_concat_v(Image.open(part[0]), Image.open(part[1])).save(f'{top}on{down}.png')


for part in permutations(players, 3):
    top = str(players.index(part[0]) + 1) \
        if players.index(part[0]) <= 2 else 'other' + str(players.index(part[0]) - 2)
    middle = str(players.index(part[1]) + 1) \
        if players.index(part[1]) <= 2 else 'other' + str(players.index(part[1]) - 2)
    bottom = str(players.index(part[2]) + 1) \
        if players.index(part[2]) <= 2 else 'other' + str(players.index(part[2]) - 2)
    for pair in permutations([top, middle, bottom]):
        if int(pair[0].replace('other', '')) == int(pair[1].replace('other', '')):
            break
    else:
        print(top, middle, bottom)
        get_concat_v(Image.open(part[0]), Image.open(part[1])).save(f'{top}on{middle}.png')
        second = Image.open(f'{top}on{middle}.png')
        get_concat_v(second, Image.open(part[2])).save(f'{top}on{middle}on{bottom}.png')