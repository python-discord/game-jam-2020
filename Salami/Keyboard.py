
import arcade

class Keyboard:
    def __init__(self):

        self.keys = {
            "up": Key(arcade.key.UP, arcade.key.W),
            "down": Key(arcade.key.DOWN, arcade.key.S),
            "left": Key(arcade.key.LEFT, arcade.key.A),
            "right": Key(arcade.key.RIGHT, arcade.key.D),
            "jump": Key(arcade.key.SPACE)
        }

    def on_key_press(self, key: int, modifiers: int):
        for k in self.keys:
            for keyCode in self.keys.get(k).key_codes:
                if key == keyCode:
                    self.keys.get(k).pressed = True

    def on_key_release(self, key: int, modifiers: int):
        for k in self.keys:
            for keyCode in self.keys.get(k).key_codes:
                if key == keyCode:
                    self.keys.get(k).pressed = False

    def is_pressed(self, key: str):
        return self.keys.get(key).pressed

class Key:
    def __init__(self, *key_codes: int):
        self.key_codes = key_codes
        self.pressed = False
        self.clicked = False