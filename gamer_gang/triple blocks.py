from gamer_gang.mechanics.menuCrap import *
from gamer_gang.mechanics.baseLevelAndPhysics import *
from gamer_gang.dumbConstants import *


class ActualGame(arcade.Window):  # TODO: relative imports and crap
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def setup(self):
        self.menuView = MenuView()
        self.gameOver = GameOverView()
        self.levels = {1: BaseLevel()}
        self.current_view = self.menuView
        print(self.current_view)
        self.game_over = False
        self.show_view(self.current_view)

def main():
    game = ActualGame()
    game.setup()
    arcade.run()

main()
