from pathlib import Path

import arcade
from screeninfo import get_monitors
from .Display import Button, Slider
from .Display import ColourBlend as cb


class Settings(arcade.View):
    width = 1920  # get_monitors()[0].width
    height = 1080  # get_monitors()[0].height

    mouse_pressing = False

    brightness_slide = Slider(int(width * 0.1), int(height * 0.57), int(width * 0.3), int(height * 0.01),
                              name="Brightness")
    volume_slide = Slider(int(width * 0.1), int(height * 0.7), int(width * 0.3), int(height * 0.01),
                          name="Volume")

    left_key_button = Button(width * 0.2, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                             activation=lambda self: setattr(self, "binding_key", "left"), name="left_button")
    center_key_button = Button(width * 0.475, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                             activation=lambda self: setattr(self, "binding_key", "center"), name="center_button")
    right_key_button = Button(width * 0.75, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                             activation=lambda self: setattr(self, "binding_key", "right"), name="right_button")

    return_button_image = arcade.Sprite(
        filename=Path().cwd() / Path("main/Resources/settings/return_button.png"),
        scale=int(min(width, height)*0.15) / 512,
        center_x=int(width*0.075),
        center_y=int(height * 0.9),)

    return_button = Button(width*0.03, height*0.86, width*0.09, height*0.08,
                           activation=lambda: None, draw_func=lambda: None, name="menu button")

    binding_key = None
    key_binds = {"left": arcade.key.A, "center": arcade.key.S, "right": arcade.key.D}

    def __init__(self, main):
        super().__init__()
        self.main = main

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])

        self.brightness_slide.draw(self.brightness)
        self.volume_slide.draw(self.brightness)

        self.left_key_button.draw(self.brightness)
        self.center_key_button.draw(self.brightness)
        self.right_key_button.draw(self.brightness)

        self.return_button_image.alpha = int(255*self.brightness)
        self.return_button_image.draw()

        self.draw_text()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressing:
            self.brightness_slide.update_slide(x, y)
            self.volume_slide.update_slide(x, y)

    def on_mouse_press(self, x, y, button, modifiers):  # Click options / volume & brightness slider
        self.mouse_pressing = True
        self.brightness_slide.pressing = self.brightness_slide.hit_box(x, y)
        self.volume_slide.pressing = self.volume_slide.hit_box(x, y)

        if self.left_key_button.pressed(x, y):
            self.left_key_button(self)
        elif self.center_key_button.pressed(x, y):
            self.center_key_button(self)
        elif self.right_key_button.pressed(x, y):
            self.right_key_button(self)

        if self.return_button.pressed(x, y):
            self.main.window.show_view(self.main.menu)

    def on_mouse_release(self, x, y, button, modifiers):  # Release for sliders
        self.mouse_pressing = False
        self.brightness_slide.pressing = False
        self.volume_slide.pressing = False

    def on_key_press(self, symbol, modifiers):  # Setting key binds
        if self.binding_key in self.key_binds and (97 <= symbol <= 122 or 48 <= symbol <= 57):
            if symbol not in self.key_binds.values():
                self.key_binds[self.binding_key] = symbol
                self.binding_key = None

    def set_binding_key(self, binding_key):
        self.binding_key = binding_key

    def draw_text(self):
        arcade.draw_text("SETTINGS", self.width * 0.2, self.height * 0.8,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 8, align="center",
                         width=int(self.width * 0.6))
        arcade.draw_text("BRIGHTNESS", self.width * 0.5, self.height * 0.52,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 12, align="center",
                         width=int(self.width * 0.6))
        arcade.draw_text("VOLUME", self.width * 0.5, self.height * 0.65,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 12, align="center",
                         width=int(self.width * 0.6))

        arcade.draw_text(chr(self.key_binds["left"]).upper(),
                         self.width * 0.178, self.height * 0.105,
                         cb.brightness([0, 0, 0], self.brightness),
                         min(self.width, self.height) / 16, align="center",
                         width=int(self.width * 0.1))
        arcade.draw_text(chr(self.key_binds["center"]).upper(),
                         self.width * 0.453, self.height * 0.105,
                         cb.brightness([0, 0, 0], self.brightness),
                         min(self.width, self.height) / 16, align="center",
                         width=int(self.width * 0.1))
        arcade.draw_text(chr(self.key_binds["right"]).upper(),
                         self.width * 0.728, self.height * 0.105,
                         cb.brightness([0, 0, 0], self.brightness),
                         min(self.width, self.height) / 16, align="center",
                         width=int(self.width * 0.1))

        arcade.draw_text("LEFT", self.width * 0.103, self.height * 0.2,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 16, align="center",
                         width=int(self.width * 0.25))
        arcade.draw_text("CENTER", self.width * 0.378, self.height * 0.2,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 16, align="center",
                         width=int(self.width * 0.25))
        arcade.draw_text("RIGHT", self.width * 0.653, self.height * 0.2,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 16, align="center",
                         width=int(self.width * 0.25))

        arcade.draw_text("KEY BINDS", self.width * 0.3, self.height * 0.38,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 12, align="center",
                         width=int(self.width * 0.4))

        arcade.draw_text("Press the button of the input channel you want to assign a new button too,\n"
                         " then press the key you want that input to be assigned to",
                         self.width * 0.1, self.height * 0.32,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 32, align="center",
                         width=int(self.width * 0.8))

    @property
    def volume(self):
        return self.volume_slide()

    @property
    def brightness(self):
        return self.brightness_slide()
