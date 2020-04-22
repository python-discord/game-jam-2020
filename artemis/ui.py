import arcade
from PIL import Image, ImageFont, ImageDraw

from constants import ASSETS, WIDTH, HEIGHT, FONT


class IconButton():
    def __init__(self, view, x, y, image, fun, size=64):
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


class Achievement(IconButton):
    def __init__(
            self, view, x, y, typ, level, name, description, achieved, size=64
            ):
        self.view = view
        self.state = 'normal'
        self.icon_texture = self.load_texture(
            f'achievement_type_{typ}', size//2
        )
        self.background_texture = self.load_texture(
            f'achievement_level_{level}', size
        )
        self.tooltip_texture = self.create_tooltip(name, description)
        self.center_x = x
        self.center_y = y
        self.size = size
        self.alpha = 255 if achieved else 100

    def create_tooltip(self, name, desc):
        gap = 5
        name_font = ImageFont.truetype(FONT.format('r'), 20)
        desc_font = ImageFont.truetype(FONT.format('ri'), 15)
        name_width, name_height = name_font.getsize(name)
        desc_width, desc_height = desc_font.getsize(desc)
        width = max(name_width, desc_width) + gap*2
        height = name_height + gap*3 + desc_height
        im = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(im)
        draw.text((gap, gap), name, (0, 0, 0), name_font)
        draw.text((gap, name_height + gap*2), desc, (0, 0, 0), desc_font)
        return arcade.Texture(name+'\n'+desc, im)

    def on_draw(self):
        self.background_texture.draw_scaled(
            self.center_x, self.center_y, alpha=self.alpha
        )
        self.icon_texture.draw_scaled(
            self.center_x, self.center_y, alpha=self.alpha
        )
        if self.state == 'hover':
            x = self.right + self.tooltip_texture.width/2 - 15
            y = self.bottom - self.tooltip_texture.height/2 + 15
            self.tooltip_texture.draw_scaled(x, y)
            if self not in self.view.on_top:
                self.view.on_top.append(self)
        elif self in self.view.on_top:
            self.view.on_top.remove(self)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass


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
        arcade.start_render()
        for button in self.buttons:
            button.on_draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for button in self.buttons:
            button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for button in self.buttons:
            button.on_mouse_release(x, y, button, modifiers)
