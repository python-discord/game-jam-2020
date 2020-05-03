import arcade
from .base import Base
from .util import arcade_int_to_string
from ..network import run


class Victory(Base):
    def __init__(self, display: arcade.Window):
        self.display = display

        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.sceneTime = 0
        self.ip = ""
        self.status = ""
        self.cursor_index = -1
        self.focus = None
        self.winner = ""

        self.sprite_setup()

    def sprite_setup(self):
        self.spritedict = {
            "background": arcade.Sprite(
                "assets/victory.png",
                center_x=640,
                center_y=360
            ),
            "back": arcade.Sprite(
                "./assets/back_button.png",
                scale=0.25,
                center_x=640,
                center_y=300
            )
        }
        self.spritelist.extend(list(self.spritedict.values()))

    def update(self, delta_time: float) -> None:
        self.sceneTime += delta_time

    def draw(self):
        self.spritelist.draw()
        arcade.draw_text(**{
            "text": f"{self.winner}",
            "start_x": 0, "start_y": 400,
            "color": (255, 255, 255),
            "font_size": 30,
            "align": "center",
            "width": 1280
        })

    def reset(self, winner_name) -> None:
        self.winner = winner_name

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.spritedict["back"].collides_with_point((x, y)) is True:
            self.display.change_scenes("mainMenu", startup=False)
        else:
            self.focus = None

