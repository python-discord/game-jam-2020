import arcade
from screeninfo import get_monitors
from Display.Input_Tools import Button, Slider


class Settings(arcade.View):

    width = get_monitors()[0].width
    height = get_monitors()[0].height

    mouse_x = 0
    mouse_y = 0

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])
        arcade.draw_text("SETTINGS", self.width*0.2, self.height*0.8,
                         [255, 255, 255], min(self.width, self.height)/8,
                         align="center", width=int(self.width*0.6))

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):  # Click options / volume & brightness slider
        pass

    def on_mouse_release(self, x, y, button, modifiers):  # Release for sliders
        pass

    def on_key_press(self, symbol, modifiers):  # Setting key binds
        pass


