import os
from itertools import count
from math import ceil

from PIL import Image

os.mkdir('generated')

FRAMES = 20

front = Image.open('front.png')
back = Image.open('back.png')
img_id = count(0)

for side in (front, back):
    side: Image.Image
    for i in range(int(FRAMES / 2)):
        width = ceil(side.width // (FRAMES / 2) * ((FRAMES / 2) - i + 1))
        frame = side.resize((width, side.height), Image.NEAREST)
        frame.save(f'generated/{next(img_id)}.png')
