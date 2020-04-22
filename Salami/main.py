
import arcade
import pyglet
import pyglet.gl as gl

import Level
import Keyboard
import Camera
import Maths

# For viewing memory usage
import psutil
import os

from Constants import WIDTH, HEIGHT, TITLE

class PyGameJam2020(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)

        self.frames = 0
        self.time = 0

        self.mouse_x = 0
        self.mouse_y = 0

        self.zoom_width = WIDTH
        self.zoom_height = HEIGHT

        self.camera = Camera.Camera(WIDTH, HEIGHT)
        self.keyboard = Keyboard.Keyboard()

        self.debug_test = ""

        self.set_icon(pyglet.image.load("Salami/icon.png"))

        self.set_location((self.camera.screen_width - WIDTH) // 2, (self.camera.screen_height - HEIGHT) // 2)

    def setup(self):
        arcade.set_background_color((19, 14, 30))
        self.level = Level.Level(self.camera, self.keyboard)

    def on_update(self, delta):

        self.level.update(delta)

        self.camera.scroll_to(self.level.player.center_x, self.level.player.center_y)

        if self.keyboard.is_pressed("zoom_in"):
            self.camera.zoom(0.95)
        elif self.keyboard.is_pressed("zoom_out"):
            self.camera.zoom(1/0.95)

        self.frames += 1
        self.time += delta

        if self.time >= 1:
            process = psutil.Process(os.getpid())
            
            self.debug_test = f"FPS: {self.frames}\nUsing: {process.memory_info().rss / 1000000} MB"

            self.time -= 1
            self.frames = 0

    def on_draw(self):

        arcade.start_render()

        self.camera.set_viewport()

        self.level.draw()

        self.camera.reset_viewport()

        arcade.draw_text(self.debug_test, 12, 12, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        self.keyboard.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        self.keyboard.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

def main():
    window = PyGameJam2020()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()