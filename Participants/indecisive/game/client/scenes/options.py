import arcade
from .base import Base


class Options(Base):
    def __init__(self, display):
        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.timeAlive = 0
        self.music_pressed = True
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

        }
        self.on_click()
        self.spritelist.extend(self.spritedict.values())

    def on_click(self):
        if self.music_pressed:
            self.spritedict["music"] = arcade.Sprite("./assets/music.png", scale=0.5, center_x=650,
                                                     center_y=400)
        elif not self.music_pressed:
            self.spritedict["music"] = arcade.Sprite("./assets/music_not_chosen.png", scale=0.5, center_x=650, center_y=400)

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
                self.display.music.play(0.01)
                self.music_pressed = True

            elif self.music_pressed:
                print("pause")
                self.music_pressed = False
                self.display.music.stop()
            self.display.music_bool = self.music_pressed

        #elif self.spritedict["help"].collides_with_point((x, y)) is True:
            #self.display.change_scenes("help")


