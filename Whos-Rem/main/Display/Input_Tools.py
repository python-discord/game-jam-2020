import arcade


class Button:

    def __init__(self, x, y, width, height, colour=(255, 255, 255), draw_func=None, activation=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

        if draw_func is None:
            self.draw = arcade.draw_lrtb_rectangle_filled(self.x, self.x + self.height,
                                                          self.y + self.height, self.y,
                                                          self.colour)
        else:
            self.draw = draw_func

        if activation is None:
            self.activation = lambda: None
        else:
            self.activation = activation

    def __call__(self, *args, **kwargs):
        return self.activation(*args, **kwargs)

    def pressed(self, mouse_x, mouse_y):
        if 0 <= mouse_x - self.x <= self.width:
            if 0 <= mouse_y - self.y <= self.height:
                return True

        return False


class Slider:

    def __init__(self, x, y, slide_dist, rotation="hor", colour=(255, 255, 255)):
        self.x = x
        self.y = y
        self.slide_dist = slide_dist
        self.rotation = rotation
        self.colour = colour
