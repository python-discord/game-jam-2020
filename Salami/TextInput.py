
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
        self.text_char = []
        self.char_list = arcade.SpriteList()

        self.x = 32
        self.y = 32

        self.caps = False

    def draw(self):
        # Draw text as Sprites
        self.char_list.move(self.x - len(self.char_list) * 4, self.y)
        self.char_list.draw(filter=gl.GL_NEAREST)
        self.char_list.move(-self.x + len(self.char_list) * 4, -self.y)
        
        # Draw text with arcade.draw_text
        # arcade.draw_text(
        #     "".join(self.text_char),
        #     WIDTH / 2 - (len(self.text_char) / 2) * 12, HEIGHT / 2,
        #     arcade.color.WHITE, 16)

    def on_key_press(self, key, modifiers):
        self.caps = modifiers == arcade.key.MOD_CAPSLOCK \
            or modifiers == arcade.key.MOD_SHIFT \
            or modifiers == arcade.key.MOD_CAPSLOCK + arcade.key.MOD_SHIFT

        if key == arcade.key.SPACE:
            # self.text_char.append(" ")
            # self.add_char(Textures.CHARACTERS[26])
            self.add_char(Textures.THIN_CHARS[26])
        elif key == arcade.key.BACKSPACE and len(self.char_list) > 0:
            # self.text_char.pop()
            self.char_list.pop()
        elif key == arcade.key.ENTER:
            self.text_char.append("\n")

        elif key >= 97 and key <= 122:
            if self.caps:
                self.add_char(Textures.THIN_CHARS[27 + key - 97])
            else:
                self.add_char(Textures.THIN_CHARS[key - 97])
            # self.add_char(Textures.CHARACTERS[key - 97])
            # if self.caps:
            #     self.text_char.append(LETTERS_CAPS[key - 97])
            # else:
            #     self.text_char.append(LETTERS[key - 97])
        elif key >= 44 and key <= 64:
            self.add_char(Textures.THIN_CHARS[27 * 2 + key - 44])
            # self.add_char(Textures.SYMBOLS[key - 44])
            # self.text_char.append(SYMBOLS[key - 44])

    def add_char(self, texture):
        char = arcade.Sprite()
        char.texture = texture
        char.center_x = len(self.char_list) * texture.width
        self.char_list.append(char)