
import arcade
import pyglet

class Camera:
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

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

    def set_viewport(self):
        arcade.set_viewport(
                int(self.left + int(self.x) - self.width // 2),
                int(self.right + int(self.x) - self.width // 2),
                int(self.bottom + int(self.y) - self.height // 2),
                int(self.top + int(self.y) - self.height // 2))

    def zoom(self, amount: float):
        self.zoom_width *= amount
        self.zoom_height *= amount

        self.left   = self.width - self.zoom_width
        self.right  = self.zoom_width
        self.bottom = self.height - self.zoom_height
        self.top    = self.zoom_height

        # self.left   = self.mouse_x * self.zoom_width
        # self.right  = (1 - self.mouse_x) * self.zoom_width
        # self.bottom = self.mouse_y * self.zoom_height
        # self.top    = (1 - self.mouse_y) * self.zoom_height