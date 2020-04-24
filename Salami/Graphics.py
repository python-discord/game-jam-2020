
from typing import Dict

import arcade

import Textures

SYMBOLS_0 = " !\"#£$%&'()*+" # 32-43
SYMBOLS = ",-./0123456789:;<=>?@" # 44-64

LETTERS = "abcdefghijklmnopqrstuvwxyz" # 97-122
LETTERS_CAPS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

MAX_CACHE_SIZE = 12

CHARS_COMBINED = \
    "abcdefghijklmnopqrstuvwxyz "\
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ "\
    ",-./0123456789:;<=>?@"

char_cache: Dict[str, arcade.Sprite] = dict()
for char in CHARS_COMBINED:
    char_cache[char] = []

class CharSprite(arcade.Sprite):
    def __init__(self, character):
        super().__init__()
        self.character = character

def create_text_list(str, x, y):
    list = arcade.SpriteList()
    for i, char in enumerate(str):
        if char in CHARS_COMBINED:
            char_sprite = get_char_sprite(char)
            char_sprite.texture = Textures.THIN_CHARS[CHARS_COMBINED.find(char)]
            char_sprite.left = x + i * char_sprite.texture.width
            char_sprite.bottom = y
            list.append(char_sprite)
    return list

def add_to_text_list(str, list, x, y):
    for i, char in enumerate(str):
        if char in CHARS_COMBINED:
            char_sprite = get_char_sprite(char)
            char_sprite.texture = Textures.THIN_CHARS[CHARS_COMBINED.find(char)]
            char_sprite.left = x + i * char_sprite.texture.width
            char_sprite.bottom = y
            list.append(char_sprite)

def empty_text_list(list):
    global char_cache
    while len(list) > 0:
        item = list.pop()
        if len(char_cache[item.character]) < MAX_CACHE_SIZE:
            char_cache[item.character].append(item)

def get_char_sprite(character):
    global char_cache
    if char_cache[character]:
        return char_cache[character].pop()
    else:
        return CharSprite(character)