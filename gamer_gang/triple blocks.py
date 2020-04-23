from gamer_gang.mechanics.menuCrap import *
from gamer_gang.mechanics.blockPhysics import *
from gamer_gang.dumbConstants import *


class ActualGame(arcade.Window):  # TODO: relative imports and crap
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.menuView = MenuView()
        self.gameOver = GameOverView()
        self.levels = Level()

    def setup(self):
        self.current_view = self.levels
        self.game_over = False
        self.show_view(self.current_view)

def main():
    game = ActualGame()
    game.setup()
    arcade.run()

main()
