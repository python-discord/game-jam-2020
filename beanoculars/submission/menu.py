import arcade

from submission.gameConstants import *
from submission.game import GameView


class MenuView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()

        self.x = None
        self.y = None
        self.title_screen = None
        self.keyText = None
        self.text_ur = None
        self.frames = None
        self.screen = None
        self.title = None

    def on_show(self):
        path = PATH['img'] / 'icons' / 'titleScreen'
        self.x, self.y = self.window.get_size()

        self.title_screen = arcade.SpriteList(is_static=True)

        src = path / 'beanWhite.png'
        imageSprite = arcade.Sprite(src, center_x=80, center_y=450)
        self.title_screen.append(imageSprite)

        src = path / 'pythonArcadeWhite.png'
        imageSprite = arcade.Sprite(src, center_x=950, center_y=35)
        self.title_screen.append(imageSprite)

        src = path / 'title.png'
        imageSprite = arcade.Sprite(src, center_x=self.x / 2, center_y=self.y / 2 + 60)
        self.title_screen.append(imageSprite)

        src = path / 'title.png'
        self.title = arcade.Sprite(src, scale=0.5, center_x=100, center_y=430)

        self.keyText = 'press any key to continue'
        self.text_ur = 60
        self.frames = 0

        self.screen = 0

        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):

        arcade.start_render()
        if self.screen == 0:
            self.title_screen.draw()
            arcade.draw_text(self.keyText, self.x / 2, 110, arcade.csscolor.WHITE, 16,
                             font_name='arial', anchor_x='center', bold=True)
            arcade.draw_text("press 'esc' to exit", self.x / 2, 80, arcade.csscolor.WHITE, 14,
                             font_name='arial', anchor_x='center', bold=True)

        if self.screen == 1:
            self.title.draw()
            arcade.draw_text('press any key to continue...', self.x - 200, 10, arcade.csscolor.WHITE, 12,
                             font_name='arial')

            arcade.draw_text('HEY, YOU!', 512, 380, arcade.csscolor.WHITE, 30,
                             font_name='arial', anchor_x='center')
            arcade.draw_text("As you know, the recent nuclear accident in the woods has made some insects enormous.",
                             512, 300, anchor_x='center', color=arcade.csscolor.WHITE, font_size=15, font_name='arial')
            arcade.draw_text("The scientists that studied the case say that the mutant bugs are multiplying really "
                             "quick, and that it will only worsen.",
                             512, 275, anchor_x='center', color=arcade.csscolor.WHITE, font_size=15, font_name='arial')
            arcade.draw_text("The horrendous insects recently started being interested in coming into town, for the"
                             " food, I guess.",
                             512, 250, anchor_x='center', color=arcade.csscolor.WHITE, font_size=15, font_name='arial')
            arcade.draw_text("The scientists developed new automatic turrets to exterminate them, but they are so big,"
                             , 512, 225, anchor_x='center', color=arcade.csscolor.WHITE, font_size=15,
                             font_name='arial')
            arcade.draw_text("that we need a helicopter to move them.",
                             512, 200, anchor_x='center', color=arcade.csscolor.WHITE, font_size=15, font_name='arial')
            arcade.draw_text("YOU are the last pilot of this town and you have to protect the people!",
                             512, 150, anchor_x='center', color=arcade.csscolor.WHITE, font_size=20, font_name='arial')

        if self.screen == 2:
            self.title.draw()
            arcade.draw_text('press any key to continue...', self.x - 200, 10, arcade.csscolor.WHITE, 12,
                             font_name='arial')

            arcade.draw_text('CONTROLS', 512, 380, arcade.csscolor.WHITE, 30,
                             font_name='arial', anchor_x='center')

            arcade.draw_text('Q:', 175, 300, arcade.csscolor.WHITE, 20, font_name='arial', anchor_x='right')
            arcade.draw_text('Pick turrets up / Place them down', 200, 300, arcade.csscolor.WHITE, 20, font_name='arial')
            arcade.draw_text('Enter:', 175, 225, arcade.csscolor.WHITE, 20, font_name='arial', anchor_x='right')
            arcade.draw_text('Start next wave', 200, 225, arcade.csscolor.WHITE, 20, font_name='arial')
            arcade.draw_text('Mouse:', 175, 150, arcade.csscolor.WHITE, 20, font_name='arial', anchor_x='right')
            arcade.draw_text('Click on the screen to move', 200, 150, arcade.csscolor.WHITE, 20, font_name='arial')

    def on_update(self, delta_time: float):
        if self.screen == 0:
            self.frames += 1
            if self.frames < self.text_ur:
                self.keyText = 'press any key to play'

            elif self.frames < 2 * self.text_ur:
                self.keyText = 'press any key to play.'

            elif self.frames < 3 * self.text_ur:
                self.keyText = 'press any key to play..'

            elif self.frames < 4 * self.text_ur:
                self.keyText = 'press any key to play...'
            else:
                self.frames = 0

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            quit()

        else:
            self.screen += 1
            if self.screen == 3:
                game_view = GameView()
                game_view.setup()
                self.window.show_view(game_view)
