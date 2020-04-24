
import arcade
import pyglet
import pyglet.gl as gl

import Level
import Keyboard
import Camera
import Maths
import Textures
import Graphics

# For viewing memory usage
import psutil
import os

from TextInput import TextInput
from Constants import WIDTH, HEIGHT, TITLE

class PyGameJam2020(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        
        arcade.set_background_color((19, 14, 30))

        self.frames = 0
        self.time = 0

        self.debug_text = ""
        self.debug = True
        self.debug_text_list = Graphics.create_text_list(self.debug_text, 12, 12)

        self.process = psutil.Process(os.getpid())

        self.set_icon(pyglet.image.load("Salami/icon.png"))

        self.text_input = TextInput()

        self.camera = Camera.Camera(WIDTH, HEIGHT)
        self.keyboard = Keyboard.Keyboard()

        self.set_location((self.camera.screen_width - WIDTH) // 2, (self.camera.screen_height - HEIGHT) // 2)


    def setup(self):
        
        self.level = Level.Level(self.camera, self.keyboard)

    def on_update(self, delta):

        self.level.update(delta)

        self.camera.scroll_to(self.level.player.center_x, self.level.player.center_y)

        # self.text_input.x = self.level.player.center_x
        # self.text_input.y = self.level.player.center_y + 8

        if self.keyboard.is_pressed("zoom_in"):
            self.camera.zoom(0.95)
        elif self.keyboard.is_pressed("zoom_out"):
            self.camera.zoom(1/0.95)

        if self.debug:
            
            self.frames += 1
            self.time += delta

            if self.time >= 1:
                self.debug_text = f"FPS: {self.frames} | Using: {round(self.process.memory_info().rss / 1000000, 2)} MB"
                # self.debug_text_list = Graphics.create_text_list(self.debug_text, 12, 12)
                Graphics.empty_text_list(self.debug_text_list)
                Graphics.add_to_text_list(self.debug_text, self.debug_text_list, 12, 12)
                print(self.debug_text)
                self.time -= 1
                self.frames = 0

    def on_draw(self):

        arcade.start_render()

        self.camera.set_viewport()

        self.level.draw()

        # self.text_input.draw()

        if self.debug:
            self.camera.reset_viewport()
            self.debug_text_list.draw(filter=gl.GL_NEAREST)
            # arcade.draw_text(self.debug_text, 12, 12, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        self.keyboard.on_key_press(key, modifiers)
    
    def on_key_release(self, key, modifiers):
        self.keyboard.on_key_release(key, modifiers)
        # self.text_input.on_key_press(key, modifiers)

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