import arcade
from PIL import Image

from constants import ASSETS, WIDTH, HEIGHT, FONT


class ViewButton(arcade.gui.TextButton):
    def __init__(self, view, x, y, text, switch_to, width=100, height=40):
        super().__init__(x, y, width, height, text, theme=view.theme)
        self.window = view.window
        self.switch_to = switch_to

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.window.show_view(self.switch_to())


class IconButton(arcade.Sprite):
    def __init__(self, x, y, view, image, fun, size=64):
        super().__init__(center_x=x, center_y=y)
        self.view = view
        self.texture = self.load_texture(image, size)
        self.fun = fun

    def load_texture(self, file, size=32):
        im = Image.open(f'{ASSETS}{file}.png').resize((size, size))
        return arcade.Texture(file, im)

    def on_mouse(self, x, y):
        x += arcade.get_viewport()[0]
        if self.left <= x <= self.right and self.bottom <= y <= self.top:
            self.fun()


class View(arcade.View):
    def __init__(self):
        super().__init__()
        self.theme = arcade.gui.Theme()
        image = ASSETS + 'button_{}.png'
        self.theme.add_button_textures(
            image.format('normal'), image.format('hover'),
            image.format('active'), image.format('locked')
        )
        self.theme.set_font(24,  (0, 0, 0), FONT.format('r'))

    def on_show(self):
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)