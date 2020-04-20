import arcade


class EventGetter(arcade.View):
    mouse_x = 0
    mouse_y = 0
    pressed_keys = []
    mouse_button_pressed = None

    @classmethod
    def on_key_press(cls, symbol, modifiers):
        if symbol not in cls.pressed_keys:
            cls.pressed_keys.append(symbol)

    @classmethod
    def on_key_release(cls, _symbol, _modifiers):
        if _symbol in cls.pressed_keys:
            cls.pressed_keys.remove(_symbol)

    @classmethod
    def on_mouse_motion(cls, x, y, dx, dy):
        cls.mouse_x = x
        cls.mouse_y = y

    @classmethod
    def on_mouse_press(cls, x, y, button, modifiers):
        cls.mouse_button_pressed = button

    @classmethod
    def on_mouse_release(cls, x, y, button, modifiers):
        if cls.mouse_button_pressed == button:
            cls.mouse_button_pressed = None


class EventHandler:
    left_game_button = arcade.key.A
    center_game_button = arcade.key.S
    right_game_button = arcade.key.D

    @classmethod
    def update_events(cls):
        pass

    @classmethod
    def get_game_buttons_pressed(cls) -> "tuple of channels active <left, center, right>":
        left_pressed = cls.left_game_button in EventGetter.pressed_keys
        center_pressed = cls.center_game_button in EventGetter.pressed_keys
        right_pressed = cls.right_game_button in EventGetter.pressed_keys

        return left_pressed, center_pressed, right_pressed

    @property
    def mouse_pos(self):
        return EventGetter.mouse_x, EventGetter.mouse_y


class Button:

    def __init__(self, x_pos, y_pos, width, height, colour=(255, 255, 255), action=None, draw_func=None, name=None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.colour = colour

        if action is None:
            self.action = lambda: None
        else:
            self.action = action

        if draw_func is None:
            self.draw = lambda: arcade.draw_lrtb_rectangle_filled(self.x_pos, self.x_pos + self.width,
                                                                  self.y_pos + self.height, self.y_pos,
                                                                  self.colour)
        else:
            self.draw = draw_func

        if name is None:
            self.name = "button"
        else:
            self.name = name

    def __call__(self):
        return self.action()

    def __eq__(self, other):
        if self.name == "button":
            raise AttributeError("Cannot compare name to default name 'button'")
        return self.name == other

    def is_pressed(self):
        if 0 <= EventHandler.mouse_pos[0] - self.x_pos <= self.width:
            if 0 <= EventHandler.mouse_pos[1] - self.y_pos <= self.height:
                return True

        return False
