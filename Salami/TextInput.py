
import arcade
import pyglet.gl as gl

from Constants import WIDTH, HEIGHT
import Textures

SYMBOLS_0 = " !\"#£$%&'()*+" # 32-43
SYMBOLS = ",-./0123456789:;<=>?@" # 44-64

LETTERS = "abcdefghijklmnopqrstuvwxyz" # 97-122
LETTERS_CAPS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class TextInput:

    def __init__(self):
        self.char_list = arcade.SpriteList()

        self.x = 32
        self.y = 32

        self.caps = False

    def draw(self):
        # Draw text as Sprites
        self.char_list.move(self.x - len(self.char_list) * 4, self.y)
        self.char_list.draw(filter=gl.GL_NEAREST)
        self.char_list.move(-self.x + len(self.char_list) * 4, -self.y)

    def on_key_press(self, key, modifiers):
        self.caps = modifiers == arcade.key.MOD_CAPSLOCK \
            or modifiers == arcade.key.MOD_SHIFT \
            or modifiers == arcade.key.MOD_CAPSLOCK + arcade.key.MOD_SHIFT

        if key == arcade.key.SPACE:
            # self.add_char(Textures.CHARACTERS[26])
            self.add_char(Textures.THIN_CHARS[26])
        elif key == arcade.key.BACKSPACE and len(self.char_list) > 0:
            self.char_list.pop()

        elif key >= 97 and key <= 122:
            if self.caps:
                self.add_char(Textures.THIN_CHARS[27 + key - 97])
            else:
                self.add_char(Textures.THIN_CHARS[key - 97])
            # self.add_char(Textures.CHARACTERS[key - 97])
        elif key >= 44 and key <= 64:
            self.add_char(Textures.THIN_CHARS[27 * 2 + key - 44])
            # self.add_char(Textures.SYMBOLS[key - 44])

    def add_char(self, texture):
        char = arcade.Sprite()
        char.texture = texture
        char.center_x = len(self.char_list) * texture.width
        self.char_list.append(char)