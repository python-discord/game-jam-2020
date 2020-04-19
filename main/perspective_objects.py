import arcade
from screeninfo import get_monitors


class Shape:

    screen_width_center = get_monitors()[0].width

    def __init__(self, x, y, scale_size, dims, dist, colour, speed):
        """
        Note: dims is a relative ratio to scale size, if you want a rectangle which
        grows to a size of 400x200 its recommended you set scale_size to 400 and
        dims to [1, 0.5] because at its largest value, width will be 400*1 = 400
        and height will be 400*0.5 = 200
        """
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


class ShapeManager:
    @staticmethod
    def manage_shapes(shapes: "list of shape objects") -> "list of updated shapes":
        for shape in shapes:
            if shape.removable:
                shapes.remove(shape)
            else:
                shape.update()

        return shapes

    @staticmethod
    def create_shape(note, total_notes=3, colour=(255, 0, 0)) -> Shape:
        final_spacing = int(get_monitors()[0].width * 0.6)
        central_spacing = final_spacing // total_notes
        width = int(central_spacing * 0.45)
        x_pos = int(central_spacing * (note / total_notes)) - central_spacing // 2
        y_pos = int(get_monitors()[0].height * 0.8)
        new_shape = Shape(x_pos, y_pos, width, [1, 0.5], 400, colour, 2)

        return new_shape

    @staticmethod
    def renderer(shape: Shape):
        shape.draw()
        return

    @classmethod
    def draw_all_shapes(cls, shapes: "list of shape objects"):
        list(map(cls.renderer, shapes))
