from pathlib import Path
from sys import path
path.append(str(Path(__file__).parent.parent))
from gamer_gang.epicAssets.menuCrap import *
from gamer_gang.epicAssets.baseLevelAndPhysics import *
from gamer_gang.dumbConstants import *

class ActualGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        self.sfx = {"jump": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/jump.wav"),
                    "star": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/star.wav"),
                    "void": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/dropVoid.wav"),
                    "sting": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/beeSting.wav"),
                    "lost": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/levelLost.wav"),
                    "win": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/levelPass.wav"),
                    "spike": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/spike.wav"),
                    "level music": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/background.wav"),
                    "menu music": arcade.load_sound(str(Path(__file__).parent) + "/epicAssets/sounds/menu.wav")}
        self.currLevel = None

    def setup(self):
        self.menuView = MenuView()
        self.gameOver = GameOverView()
        self.levels = {1: Level(1), 2: Level(2), 3: Level(3), 4: Level(4), 5: Level(5)}
        self.game_over = False
        self.deathCause = None
        self.show_view(self.menuView)

def main():
    game = ActualGame()
    game.setup()
    arcade.run()

main()
