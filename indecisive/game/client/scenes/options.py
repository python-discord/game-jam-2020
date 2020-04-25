import arcade
from .base import Base
from .sound import Sound

class Options(Base):
    def __init__(self, display):
        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.timeAlive = 0
        self.music_pressed = False
        self.fullscreen_pressed = False
        self.display = display
        self.sprite_setup()

    def sprite_setup(self):
        self.spritedict = {
            "exit": arcade.Sprite(
                "./assets/Exit.png",
                scale=0.25,
                center_x=640,
                center_y=120
            ),

            "title": arcade.Sprite(
                "./assets/Options.png",
                scale=0.5,
                center_x=770,
                center_y=580
            ),
            "help": arcade.Sprite(
                "./assets/help.png",
                scale=0.5,
                center_x=300,
                center_y=120
            ),
        }
        self.on_click()
        self.spritelist.extend(self.spritedict.values())

    def on_click(self):
        if not self.music_pressed:
            self.spritedict["music"] = arcade.Sprite("./assets/music_not_chosen.png", scale=0.5, center_x=650,
                                                     center_y=400)
        elif self.music_pressed:
            self.spritedict["music"] = arcade.Sprite("./assets/music.png", scale=0.5, center_x=650, center_y=400)

        if not self.fullscreen_pressed:
            self.spritedict["Fullscreen"] = arcade.Sprite("./assets/fullscreen.png", scale=0.5, center_x=650,
                                                          center_y=260)
        elif self.fullscreen_pressed:
            self.spritedict["Fullscreen"] = arcade.Sprite("./assets/windowed.png", scale=0.5, center_x=650,
                                                          center_y=260)

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.sprite_setup()
        self.spritelist.draw()

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        print((x, y))
        if self.spritedict["exit"].collides_with_point((x, y)) is True:
            self.display.change_scenes("mainMenu")

        elif self.spritedict["music"].collides_with_point((x, y)) is True:
            if not self.music_pressed:
                print("play")
                Sound().setup(self.music_pressed)
                self.music_pressed = True
            elif self.music_pressed:
                print("pause")
                self.music_pressed = False

        elif self.spritedict["Fullscreen"].collides_with_point((x, y)) is True:
            if not self.fullscreen_pressed:
                print("fullscreen")
                self.fullscreen_pressed = True
                self.display.set_fullscreen(not self.display.fullscreen)
                self.display.set_viewport(1, 1280, 1, 720)
                width, height = self.display.get_size()
                self.display.set_viewport(0, 1280, 1, 720)

            elif self.fullscreen_pressed:
                print("windowed")
                self.display.set_fullscreen(not self.display.fullscreen)
                self.display.set_viewport(0, 1280, 0, 720)
                self.fullscreen_pressed = False

        elif self.spritedict["help"].collides_with_point((x, y)) is True:
            self.display.change_scenes("help")


