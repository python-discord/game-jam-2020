import arcade
from .base import Base
import arcade.gui


class Options(Base):
    def __init__(self, display):
        self.display = display
        self.spritelist = arcade.SpriteList()
        self.buttonlist = []
        self.spritedict = dict()
        self.timeAlive = 0
        self.theme = None
        self.setup()

    def setup_textures(self):
        normal = "./assets/normal_Button.png"
        hover = "./assets/Hovered_Button.png"
        clicked = "./assets/Hovered_Button.png"
        self.theme.add_button_textures(normal, hover, clicked)

    def setup_theme(self):
        self.theme = arcade.gui.Theme()
        self.theme.set_font(24, arcade.color.WHITE)
        self.setup_textures()

    def setup(self):
        self.setup_theme()
        self.button_setup()

    def sprite_setup(self):
        self.spritedict = {
            "back": arcade.Sprite(
                "./assets/Options.png",
                scale=0.25,
                center_x=160,
                center_y=687.5
            )
        }
        self.spritelist.extend(self.spritedict.values())

    def button_setup(self):
        self.buttonlist.append(Button("options", "main_menu", 560, 620, 400, 150, "Exit", self.theme))
        self.buttonlist.append(Button("options", "option", 600, 400, 400, 150, "Music", self.theme))
        self.buttonlist.append(Button("options", "main_menu", 500, 200, 400, 150, "Accept", self.theme))

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()


class Button(arcade.TextButton):
    def __init__(self, start_scene, next_scene, x, y, width, height, text, theme=None):
        super(Button, self).__init__(x, y, width, height, text, theme=theme)
        self.start_scene = start_scene
        self.next_scene = next_scene
        self.clicked = False

    def on_press(self):
        self.clicked = True

    def on_release(self):
        if self.clicked:
            if self.next_scene == "Exit":
                arcade.close_window()
            else:
                self.display.change_scenes(self.next_scene)
