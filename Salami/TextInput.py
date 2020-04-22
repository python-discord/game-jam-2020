
import arcade
from Constants import WIDTH, HEIGHT

class TextInput:

    def __init__(self):
        self.text_char = []

        self.symbols = list("0123456789:;<=>?@") # 48-64

        self.letters = "abcdefghijklmnopqrstuvwxyz" # 97-122
        self.letters_caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        self.caps = False

    def draw(self):
        arcade.draw_text(
            "".join(self.text_char),
            WIDTH / 2 - (len(self.text_char) / 2) * 12, HEIGHT / 2,
            arcade.color.WHITE, 16)

    def on_key_press(self, key, modifiers):
        self.caps = modifiers == arcade.key.MOD_CAPSLOCK \
            or modifiers == arcade.key.MOD_SHIFT \
            or modifiers == arcade.key.MOD_CAPSLOCK + arcade.key.MOD_SHIFT

        if key == arcade.key.SPACE:
            self.text_char.append(" ")
        elif key == arcade.key.BACKSPACE:
            self.text_char.pop()
        elif key == arcade.key.ENTER:
            self.text_char.append("\n")

        elif key >= 97 and key <= 122:
            if self.caps:
                self.text_char.append(self.letters_caps[key - 97])
            else:
                self.text_char.append(self.letters[key - 97])
        elif key >= 48 and key <= 64:
            self.text_char.append(self.symbols[key - 48])
