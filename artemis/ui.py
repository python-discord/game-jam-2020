import arcade
from PIL import Image

from constants import ASSETS, WIDTH, HEIGHT, FONT


class IconButton():
    def __init__(self, view, x, y, image, fun, size=64):
        print(id(self))
        self.view = view
        self.state = 'normal'
        self.icon_texture = self.load_texture(image, size//2)
        self.textures = {}
        for state in ('normal', 'pressed', 'hover'):
            self.textures[state] = self.load_texture('button_'+state, size)
        self.fun = fun
        self.center_x = x
        self.center_y = y
        self.size = size

    def load_texture(self, file, size):
        im = Image.open(f'{ASSETS}{file}.png').resize((size, size))
        return arcade.Texture(file, im)

    def on_draw(self):
        self.textures[self.state].draw_scaled(self.center_x, self.center_y)
        self.icon_texture.draw_scaled(self.center_x, self.center_y)

    @property
    def left(self):
        return self.center_x - self.size/2

    @property
    def right(self):
        return self.center_x + self.size/2

    @property
    def top(self):
        return self.center_y + self.size/2

    @property
    def bottom(self):
        return self.center_y - self.size/2

    def on_mouse_press(self, x, y, button, modifiers):
        x += arcade.get_viewport()[0]
        if self.left <= x <= self.right and self.bottom <= y <= self.top:
            self.state = 'pressed'

    def on_mouse_motion(self, x, y, dx, dy):
        x += arcade.get_viewport()[0]
        if self.left <= x <= self.right and self.bottom <= y <= self.top:
            self.state = 'hover'
        else:
            self.state = 'normal'

    def on_mouse_release(self, x, y, button, modifiers):
        if self.state == 'pressed':
            self.fun()
            self.state = 'normal'


class ViewButton(IconButton):
    def __init__(self, view, x, y, image, switch_to, size=64):
        self.switch_to = switch_to
        super().__init__(view, x, y, image, self.switch)

    def switch(self):
        self.view.window.show_view(self.switch_to())


class View(arcade.View):
    reset_viewport = True

    def __init__(self):
        super().__init__()
        if type(self).reset_viewport:
            arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        self.buttons = []
        self.hide_mouse_after = 1

    def on_update(self, td):
        self.hide_mouse_after -= td
        if self.hide_mouse_after < 0:
            self.window.set_mouse_visible(False)
            for button in self.buttons:
                if button.state != 'normal':
                    self.window.set_mouse_visible(True)
                    break

    def on_mouse_motion(self, x, y, dx, dy):
        self.hide_mouse_after = 1
        self.window.set_mouse_visible(True)
        for button in self.buttons:
            button.on_mouse_motion(x, y, dx, dy)

    def on_draw(self):
        for button in self.buttons:
            button.on_draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for button in self.buttons:
            button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for button in self.buttons:
            button.on_mouse_release(x, y, button, modifiers)