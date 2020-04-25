
import arcade

class Keyboard:

    class Key:
        def __init__(self, key_codes):
            self.key_codes = list(key_codes)
            self.pressed = False
            self.clicked = False

    def __init__(self):

        self.mouse_x = 0
        self.mouse_y = 0

        self.key_codes_list = {}

        self.keys = {
            # "up": self.Key(arcade.key.UP, arcade.key.W),
            # "down": self.Key(arcade.key.DOWN, arcade.key.S),
            # "left": self.Key(arcade.key.LEFT, arcade.key.A),
            # "right": self.Key(arcade.key.RIGHT, arcade.key.D),
            # "jump": self.Key(arcade.key.SPACE)
        }

        self.add_key("up", arcade.key.UP, arcade.key.W)
        self.add_key("down", arcade.key.DOWN, arcade.key.S)
        self.add_key("left", arcade.key.LEFT, arcade.key.A)
        self.add_key("right", arcade.key.RIGHT, arcade.key.D)
        self.add_key("jump", arcade.key.SPACE)

        self.add_key("attack", arcade.key.J)
        self.add_key("dash", arcade.key.K)
        self.add_key("l", arcade.key.L)
        self.add_key("sprint", arcade.key.LSHIFT)
        self.add_key("e", arcade.key.E)

        self.add_key("zoom_out", arcade.key.MINUS)
        self.add_key("zoom_in", arcade.key.EQUAL)
        self.add_key("fullscreen", arcade.key.F10)
        self.add_key("esc", arcade.key.ESCAPE)

    def on_key_press(self, key: int, modifiers: int):
        if self.key_codes_list.get(key):
            self.key_codes_list.get(key).pressed = True

    def on_key_release(self, key: int, modifiers: int):
        if self.key_codes_list.get(key):
            self.key_codes_list.get(key).pressed = False

    def on_mouse_move(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def is_pressed(self, key):
        return self.keys.get(key).pressed

    def add_key(self, key, *key_codes: int):
        if self.keys.get(key):
            for key_code in key_codes:
                self.keys[key].key_codes.append(key_code)
        else:
            self.keys[key] = self.Key(key_codes)

        for key_code in key_codes:
            self.key_codes_list[key_code] = self.keys[key]
