
import arcade
import pyglet

import Maths

class Camera:
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.width_center = width // 2
        self.height_center = height // 2

        self.x = 0
        self.y = 0

        # Get the display width and height
        screen = pyglet.canvas.Display().get_default_screen()

        self.screen_width = screen.width
        self.screen_height = screen.height
        
        self.zoom_width = width
        self.zoom_height = height

        self.mouse_x = 0
        self.mouse_y = 0

        self.left = 0
        self.right = width
        self.bottom = 0
        self.top = height

        self.camera_lag = 2
        self.scroll_step = 0.005
        self.scroll_min_step = 0.1
        self.scroll_curr_step = 0.2

        self.old_x = 0
        self.old_y = 0

    def reset_viewport(self):
        arcade.set_viewport(0, self.width, 0, self.height)

    def set_viewport(self):
        # left = int(self.left + int(self.x) - self.width_center)
        # right = int(self.right + int(self.x) - self.width_center)
        # bottom = int(self.bottom + int(self.y) - self.height_center)
        # top = int(self.top + int(self.y) - self.height_center)

        left = self.left + self.x - self.width_center
        right = self.right + self.x - self.width_center
        bottom = self.bottom + self.y - self.height_center
        top = self.top + self.y - self.height_center
        
        arcade.set_viewport(left, right, bottom, top)

    def scroll_to(self, x, y):

        diff_x = self.x - x
        diff_y = self.y - y

        # if diff_x > 128 \
        #     or diff_y > 128 \
        #     or (x == self.old_x and y == self.old_y and self.scroll_curr_step < 1
        # ):
        #     self.scroll_curr_step += self.scroll_step
        # else:
        #     self.scroll_curr_step = self.scroll_min_step

        if abs(diff_x) > self.camera_lag:
            self.x = self.x - self.scroll_curr_step * diff_x
            # self.x = Maths.lerp(self.x, x, 0.95)
            # self.x = self.x - Maths.smoothstep(0, 1, self.scroll_curr_step) * diff_x
        if abs(diff_y) > self.camera_lag:
            self.y = self.y - self.scroll_curr_step * diff_y
            # self.y = Maths.lerp(self.y, y, 0.95)
            # self.y = self.y - Maths.smoothstep(0, 1, self.scroll_curr_step) * diff_y

        self.old_x = x
        self.old_y = y

    def zoom(self, amount: float):
        self.zoom_width *= amount
        self.zoom_height *= amount

        if self.zoom_width < self.width * 0.55:
            self.zoom_width = self.width * 0.55 + 0.1
        if self.zoom_height < self.height * 0.55:
            self.zoom_height = self.height * 0.55 + 0.1

        self.left   = self.width - self.zoom_width
        self.right  = self.zoom_width
        self.bottom = self.height - self.zoom_height
        self.top    = self.zoom_height

        # self.left   = self.mouse_x * self.zoom_width
        # self.right  = (1 - self.mouse_x) * self.zoom_width
        # self.bottom = self.mouse_y * self.zoom_height
        # self.top    = (1 - self.mouse_y) * self.zoom_height