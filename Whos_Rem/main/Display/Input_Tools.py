import arcade
from .Utility import ColourBlend as cb


class Button:
    def __init__(self, x, y, width, height, colour=(255, 255, 255), draw_func=None, activation=None, name="button"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.name = name

        if draw_func is None:
            self.draw = lambda brightness: arcade.draw_lrtb_rectangle_filled(self.x, self.x + self.height,
                                                                             self.y + self.height, self.y,
                                                                             cb.brightness(self.colour, brightness))
        else:
            self.draw = lambda brightness, *args, **kwargs: draw_func(brightness, *args, **kwargs)

        if activation is None:
            self.activation = lambda: None
        else:
            self.activation = activation

    def __call__(self, *args, **kwargs):
        return self.activation(*args, **kwargs)

    def __eq__(self, other):
        if self.name == "button":
            raise AttributeError("Cannot compare name if name is default value 'button'")
        else:
            return self.name == other

    def pressed(self, mouse_x, mouse_y):
        if 0 <= mouse_x - self.x <= self.width:
            if 0 <= mouse_y - self.y <= self.height:
                return True

        return False


class Slider:

    def __init__(self, x, y, width, height, rotation="hor", colour=(255, 255, 255), start_value=1.0, name="slider"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.colour = colour
        self.pressing = True
        self.slide_dist = int(width * start_value)
        self.pressing = False
        self.name = name

    def __call__(self):
        return self.pct_value

    def __eq__(self, other):
        if self.name == "slider":
            raise AttributeError("Cannot compare name if name is default value 'slider'")
        return self.name == other

    @property
    def pct_value(self):
        return self.slide_dist / self.width

    @property
    def slide_dist(self):
        return self.__slide_dist

    @slide_dist.setter
    def slide_dist(self, value):
        if self.pressing:
            if value < 0:
                self.__slide_dist = 0
            elif value > self.width:
                self.__slide_dist = self.width
            else:
                self.__slide_dist = value

    def update_slide(self, mouse_x, mouse_y):
        if self.rotation == "hor":
            self.slide_dist = mouse_x - self.x
        else:
            self.__slide_dist = mouse_y - self.y

    def hit_box(self, mouse_x, mouse_y):
        if self.rotation == "hor":
            if 0 <= mouse_x - self.x <= self.width:
                if -1.5 * self.height <= mouse_y - self.y <= 2.5 * self.height:
                    return True
        else:
            if -1.5 * self.width <= mouse_x - self.x <= 2.5 * self.width:
                if 0 <= mouse_y - self.y <= self.height:
                    return True

        return False

    def draw(self, brightness):
        arcade.draw_lrtb_rectangle_filled(self.x, self.x + self.width,
                                          self.y + self.height, self.y,
                                          cb.brightness(self.colour, brightness))
        if self.rotation == "hor":
            arcade.draw_circle_filled(self.x + self.slide_dist,
                                      self.y + self.height // 2,
                                      self.height * 3.2, [0, 0, 0])
            arcade.draw_circle_filled(self.x + self.slide_dist,
                                      self.y + self.height // 2,
                                      self.height * 3,
                                      cb.brightness(self.colour, brightness))
        else:
            arcade.draw_circle_filled(self.x + self.width // 2,
                                      self.y + self.slide_dist,
                                      self.width * 3.2, [0, 0, 0])
            arcade.draw_circle_filled(self.x + self.width // 2,
                                      self.y + self.slide_dist,
                                      self.width * 3,
                                      cb.brightness(self.colour, brightness))

