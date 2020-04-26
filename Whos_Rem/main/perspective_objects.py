import math

import arcade
import pyautogui
from .display import ColourBlend as cb


class Shape:

    def __init__(self, x: "end position relative to center screen",
                 y: "starting y height, ends at 0",
                 screen_width_center: "screen_width // 2",
                 scale_size: "final size",
                 dims: "ratio width:height, list length 2",
                 dist: "starting 'dist' from screen, int",
                 colour: list,
                 speed: "default rate distance decreases, can be overwritten in update()",):
        """
        Note: dims is a relative ratio to scale size, if you want a rectangle which
        grows to a size of 400x200 its recommended you set scale_size to 400 and
        dims to [1, 0.5] because at its largest value, width will be 400*1 = 400
        and height will be 400*0.5 = 200
        """
        self.end_x = x
        self.start_y = y
        self.screen_width_center = screen_width_center
        self.scale_size = scale_size
        self.dims = dims
        self.dist = self.start_dist = dist
        self.colour = colour
        self.speed = speed

    @property
    def x(self):
        if self.dist > 0:
            return self.screen_width_center + math.copysign(
                int(abs(self.end_x)**(1 - self.dist/self.start_dist)), self.end_x)
        else:
            return self.end_x + self.screen_width_center

    @property
    def y(self):
        offset = int(-self.dims[1]*self.scale_size)
        if self.dist > 0:
            return self.start_y - int(self.start_y**(1 - self.dist/self.start_dist)) + offset
        else:
            return offset

    @property
    def size(self):
        if self.dist > 0:
            return int(self.scale_size**(1 - self.dist/self.start_dist))
        else:
            return self.scale_size

    def update(self, speed=None):
        if speed is None:
            self.dist -= self.speed
        else:
            self.dist -= speed

    @property
    def removable(self):
        return self.dist <= 0

    def draw(self, brightness):
        arcade.draw_rectangle_filled(self.x, self.y,
                                     int(self.dims[0] * self.size),
                                     int(self.dims[1] * self.size),
                                     cb.brightness(self.colour, brightness))


class ShapeManager:

    @classmethod
    def manage_shapes(cls, shapes: "list of shape objects", brightness, speed: float = None) -> "list of updated shapes":
        for shape in shapes:
            if shape.removable:
                shapes.remove(shape)
            else:
                shape.update(speed)

        cls.draw_all_shapes(shapes, brightness)
        return shapes

    @staticmethod
    def create_shape(note, screen_size, total_notes=3, colour=(255, 0, 0)) -> Shape:
        screen_width, screen_height = screen_size
        final_spacing = int(screen_width * 0.4)
        central_spacing = final_spacing // (total_notes - 1) if total_notes != 1 else 0
        width = int(central_spacing * 0.55)
        x_pos = int(central_spacing * note)
        y_pos = int(screen_height * 0.8)
        new_shape = Shape(x_pos, y_pos, screen_width // 2, width, [1, 0.5], 256, colour, 2)

        return new_shape

    @classmethod
    def draw_all_shapes(cls, shapes: "list of shape objects", brightness=1):
        for shape in shapes:
            shape.draw(brightness)
