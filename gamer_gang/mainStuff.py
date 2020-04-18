import arcade

width = 700
height = 600
gravity = 1

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width, height, title='GAMER GANG GAMER GANG GAMER GANG')
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

        self.heroes = arcade.SpriteList()
        self.justWalls = arcade.SpriteList()

        self.initStack = arcade.Sprite('images/completStackPlaceholder.jpg', 0.25)  # just a test
        self.initStack.center_x, self.initStack.center_y = 200, 200
        self.heroes.append(self.initStack)
        # self.spikeList = arcade.sprite_list() add these later?
        # self.enemyList = arcade.sprite_list()

        self.dumbPhysics = arcade.PhysicsEnginePlatformer(self.heroes, self.justWalls, 1)

    def on_draw(self):
        arcade.start_render()

        self.heroes.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            pass  # jump

        elif symbol == arcade.key.LEFT:
            pass  # move left

        elif symbol == arcade.key.RIGHT:
            pass

        elif symbol == arcade.key.DOWN:
            pass

        elif symbol == arcade.key.NUM_1:
            pass  # take control of the #1 hero

        elif symbol == arcade.key.NUM_2:
            pass  # hero #2

        elif symbol == arcade.key.NUM_3:
            pass  # hero #3

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            pass  # jump

        elif symbol == arcade.key.LEFT:
            pass  # move left

        elif symbol == arcade.key.RIGHT:
            pass

        elif symbol == arcade.key.DOWN:
            pass

def main():
    actualGame = Game()
    arcade.run()

main()
