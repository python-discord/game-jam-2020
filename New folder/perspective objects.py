import arcade
from screeninfo import get_monitors


class Shape:

    screen_width_center = get_monitors()[0].width

    def __init__(self, x, y, scale_size, dims, dist, colour, speed):
        # Note: dims is a relative ratio to scale size, if you want a rectangle which
        # grows to a size of 400x200 its recommended you set scale_size to 400 and
        # dims to [1, 0.5] because at its largest value, width will be 400*1 = 400
        # and height will be 400*0.5 = 200
        self.end_x = x
        self.start_y = y
        self.scale_size = scale_size
        self.dims = dims
        self.start_dist = dist
        self.dist = dist
        self.colour = colour
        self.speed = speed

    @property
    def x(self):
        if self.dist != 0:
            return self.screen_width_center + int(self.end_x**(1 - self.dist/self.start_dist))
        else:
            return self.end_x + self.screen_width_center

    @property
    def y(self):
        offset = int(-self.dims[1]*self.scale_size)
        if self.dist != 0:
            return self.start_y - int(self.start_y**(1 - self.dist/self.start_dist)) + offset
        else:
            return offset

    @property
    def size(self):
        if self.dist != 0:
            return int(self.scale_size**(1 - self.dist/self.start_dist))
        else:
            return self.scale_size

    def update(self):
        self.dist -= self.speed

    @property
    def removable(self):
        return self.dist <= 0

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y,
                                     int(self.dims[0] * self.scale_size),
                                     int(self.dims[1] * self.scale_size),
                                     self.colour)
