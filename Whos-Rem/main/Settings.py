import arcade
from screeninfo import get_monitors
from Display.Input_Tools import Button, Slider
from Display.Utility import ColourBlend as cb


class Settings(arcade.View):
    width = get_monitors()[0].width
    height = get_monitors()[0].height

    mouse_x = 0
    mouse_y = 0
    mouse_pressing = False

    brightness_slide = Slider(int(width * 0.1), int(height * 0.5), int(width * 0.3), int(height * 0.01),
                              name="Brightness")
    volume_slide = Slider(int(width * 0.1), int(height * 0.7), int(width * 0.3), int(height * 0.01), name="Volume")

    left_key_button = Button(width * 0.2, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                             activation=lambda self: self.binding_key("left"))
    center_key_button = Button(width * 0.45, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                             activation=lambda self: self.binding_key("center"))
    right_key_button = Button(width * 0.7, height * 0.1, min(width, height) * 0.1, min(width, height) * 0.1,
                             activation=lambda self: self.binding_key("right"))

    await_key_press = False
    key_binds = {"left": arcade.key.A, "center": arcade.key.S, "right": arcade.key.D}
    binding_key = None

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])
        arcade.draw_text("SETTINGS", self.width * 0.2, self.height * 0.8,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 8, align="center",
                         width=int(self.width * 0.6))

        self.brightness_slide.draw(self.brightness)
        arcade.draw_text("BRIGHTNESS", self.width * 0.5, self.height * 0.45,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 12, align="center",
                         width=int(self.width * 0.6))

        self.volume_slide.draw(self.brightness)
        arcade.draw_text("VOLUME", self.width * 0.5, self.height * 0.65,
                         cb.brightness([255, 255, 255], self.brightness),
                         min(self.width, self.height) / 12, align="center",
                         width=int(self.width * 0.6))

        self.left_key_button.draw(self.brightness)

        self.center_key_button.draw(self.brightness)

        self.right_key_button.draw(self.brightness)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        if self.mouse_pressing:
            self.brightness_slide.update_slide(self.mouse_x, self.mouse_y)
            self.volume_slide.update_slide(self.mouse_x, self.mouse_y)

    def on_mouse_press(self, x, y, button, modifiers):  # Click options / volume & brightness slider
        self.mouse_pressing = True

    def on_mouse_release(self, x, y, button, modifiers):  # Release for sliders
        self.mouse_pressing = False

    def on_key_press(self, symbol, modifiers):  # Setting key binds
        if self.await_key_press:
            if self.binding_key in self.key_binds and (97 <= symbol <= 122 or 48 <= symbol <= 57):
                self.key_binds[self.binding_key] = symbol
                self.await_key_press = False
                self.binding_key = None

    def set_binding_key(self, binding_key):
        self.await_key_press = True
        self.binding_key = binding_key

    @property
    def volume(self):
        return self.volume_slide()

    @property
    def brightness(self):
        return self.brightness_slide()
