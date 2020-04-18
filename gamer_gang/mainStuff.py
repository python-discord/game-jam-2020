import arcade

width = 700
height = 600

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width, height, title='GAMER GANG GAMER GANG GAMER GANG')
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

        self.setup()

    def setup(self):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            pass  # jump

        elif symbol == arcade.key.LEFT:
            pass  # move left

def main():
    actualGame = Game()
    actualGame.run()

main()
