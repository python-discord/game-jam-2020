
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

LOADING = 0
PLAYING = 1

class PyGameJam2020(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE, resizable=True)
        
        arcade.set_background_color((19, 14, 30))

        self.frames = 0
        self.time = 0

        self.debug_text = ""
        self.debug = True
        self.debug_text_list = Graphics.create_text_list(self.debug_text, 12, 12)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.process = psutil.Process(os.getpid())
        self.set_icon(pyglet.image.load("resources/icon.png"))

        self.text_input = TextInput()
        self.typing = False

        self.camera = Camera.Camera(WIDTH, HEIGHT)
        self.camera.zoom(20)
        self.keyboard = Keyboard.Keyboard()

        self.set_min_size(WIDTH, HEIGHT)
        self.prev_size = self.get_size()

        self.set_location(
            (self.camera.screen_width - WIDTH) // 2,
            (self.camera.screen_height - HEIGHT) // 2)

    def setup(self):
        
        self.game_state = LOADING
        self.level = Level.Level(self.camera, self.keyboard)

    def on_update(self, delta):
        # if self.game_state == PLAYING:
        self.level.update(delta)
        if self.game_state == LOADING:
            if self.camera.zoom_width > self.camera.width:
                self.camera.zoom(0.98)
            else:
                self.game_state = PLAYING
                self.level.paused = False

        self.camera.scroll_to(self.level.player.center_x, self.level.player.center_y)

        self.text_input.x = self.level.player.center_x
        self.text_input.y = self.level.player.center_y + 8

        if self.keyboard.is_pressed("zoom_in"):
            self.camera.zoom(0.98)
        elif self.keyboard.is_pressed("zoom_out"):
            self.camera.zoom(1/0.98)

        if self.debug:
            
            self.frames += 1
            self.time += delta

            if self.time >= 1:
                self.debug_text = f"FPS: {self.frames} | Using: {round(self.process.memory_info().rss / 1000000, 2)} MB"

                Graphics.empty_text_list(self.debug_text_list)
                Graphics.add_to_text_list(self.debug_text, self.debug_text_list, 12, 12)
                x0 = self.level.level_gen.current_room.x if self.level.level_gen.current_room else -1
                y0 = self.level.level_gen.current_room.y if self.level.level_gen.current_room else -1
                player_pos = (f"<{round(x0, 2)}, {round(y0, 2)}>"
                    f" <Entities: {len(self.level.entities)}>")

                Graphics.add_to_text_list(player_pos, self.debug_text_list, 12, 24)
                
                self.time -= 1
                self.frames = 0

    def on_draw(self):

        arcade.start_render()

        self.camera.set_viewport()

        self.level.draw()

        if self.typing:
            self.text_input.draw()

        self.camera.reset_viewport()

        if self.debug:
            self.debug_text_list.draw(filter=gl.GL_NEAREST)
            # arcade.draw_text(self.debug_text, 12, 12, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        self.keyboard.on_key_press(key, modifiers)

        if self.keyboard.is_pressed("fullscreen"):
            self.set_fullscreen(not self.fullscreen)

        if self.keyboard.is_pressed("esc"):
            self.level.paused = not self.level.paused
        
        if self.keyboard.is_pressed("enter"):
            self.typing = not self.typing
    
    def on_key_release(self, key, modifiers):
        self.keyboard.on_key_release(key, modifiers)
        if self.typing:
            self.text_input.on_key_press(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_resize(self, width: float, height: float):
        self.camera.resize(width, height)

        # Resize to Aspect Ratio
        # scale_x = width / self.prev_size[0]
        # scale_y = height / self.prev_size[1]
        # scale = min(scale_x, scale_y)

        # self.set_size(int(self.prev_size[0] * scale), int(self.prev_size[1] * scale))
        # self.prev_size = self.get_size()

def main():
    window = PyGameJam2020()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()