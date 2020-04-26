from pathlib import Path

import arcade
import pyautogui
from .display import Button, Slider
from .display import ColourBlend as cb


class Settings(arcade.View):
    mouse_pressing = False

    binding_key = None
    key_binds = {"left": arcade.key.A, "center": arcade.key.S, "right": arcade.key.D}

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.width, self.height = self.main.size
        width, height = self.main.size

        self.background_image = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/background.png"),
            scale=max(width / 6400, height / 3600),
            center_x=int(width * 0.5),
            center_y=int(height * 0.5),
        )

        self.brightness_slide = Slider(int(width * 0.1), int(height * 0.57), int(width * 0.3), int(height * 0.01),
                                  name="Brightness")
        self.volume_slide = Slider(int(width * 0.1), int(height * 0.7), int(width * 0.3), int(height * 0.01),
                              name="Volume")

        self.left_key_button = Button(width * 0.2, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                                 activation=lambda self: setattr(self, "binding_key", "left"), name="left_button")
        self.center_key_button = Button(width * 0.475, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                                   activation=lambda self: setattr(self, "binding_key", "center"), name="center_button")
        self.right_key_button = Button(width * 0.75, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                                  activation=lambda self: setattr(self, "binding_key", "right"), name="right_button")

        return_button_image = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/return_button.png"),
            scale=int(min(width, height) * 0.15) / 512,
            center_x=int(width * 0.075),
            center_y=int(height * 0.9), )

        self.return_button = Button(width * 0.03, height * 0.86, width * 0.09, height * 0.08,
                               activation=lambda: None, draw_func=lambda: None, name="menu button")

        settings_title = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/settings-title.png"),
            scale=int(min(width, height) * 0.2) / 128,
            center_x=int(width * 0.5),
            center_y=int(height * 0.87),
        )
        brightness_text = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/brightness.png"),
            scale=int(min(width, height) * 0.1) / 128,
            center_x=int(width * 0.8),
            center_y=int(height * 0.56),
        )
        volume_text = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/volume.png"),
            scale=int(min(width, height) * 0.14) / 128,
            center_x=int(width * 0.8),
            center_y=int(height * 0.68),
        )

        left_text = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/Left.png"),
            scale=int(min(width, height) * 0.15) / 128,
            center_x=int(width * 0.23),
            center_y=int(height * 0.25),
        )
        center_text = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/Center.png"),
            scale=int(min(width, height) * 0.15) / 128,
            center_x=int(width * 0.51),
            center_y=int(height * 0.25),
        )
        right_text = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/Right.png"),
            scale=int(min(width, height) * 0.15) / 128,
            center_x=int(width * 0.78),
            center_y=int(height * 0.25),
        )
        key_binds_text = arcade.Sprite(
            filename=Path().cwd() / Path("main/Resources/settings_menu/Key-Binds.png"),
            scale=int(min(width, height) * 0.17) / 128,
            center_x=int(width * 0.5),
            center_y=int(height * 0.45),
        )

        self.text_objects = [settings_title, brightness_text, volume_text, left_text,
                        right_text, center_text, key_binds_text, return_button_image]

    def on_draw(self):
        arcade.start_render()
        self.background_image.alpha = int(255 * self.brightness)
        self.background_image.draw()

        self.brightness_slide.draw(self.brightness)
        self.volume_slide.draw(self.brightness)

        self.left_key_button.draw(self.brightness)
        self.center_key_button.draw(self.brightness)
        self.right_key_button.draw(self.brightness)

        self.draw_text()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressing:
            self.brightness_slide.update_slide(x, y)
            self.volume_slide.update_slide(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
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

    def on_mouse_release(self, x, y, button, modifiers):
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
        alpha = int(255 * self.main.brightness)
        for item in self.text_objects:
            item.alpha = alpha
            item.draw()

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
