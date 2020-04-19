import arcade


class EventHandler:
    left_game_button = arcade.key.A
    center_game_button = arcade.key.S
    right_game_button = arcade.key.D

    @classmethod
    def update_events(cls):
        pass

    @classmethod
    def get_game_buttons_pressed(cls) -> "tuple of channels active <left, center, right>":
        left_pressed = cls.left_game_button in "<pressed keys>: list"
        center_pressed = cls.center_game_button in "<pressed keys>: list"
        right_pressed = cls.right_game_button in "<pressed keys>: list"

        return left_pressed, center_pressed, right_pressed


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
        """if 0 <= <mouse x position> - self.x_pos <= self.width:
            if 0 <= <mouse y position> - self.y_pos <= self.height:
                return True

        return False"""
