from arcade.gui import *
import random
from gamer_gang.dumbConstants import *


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.PALE_TURQUOISE)
        self.start = False

    def on_show(self):
        arcade.set_viewport(0, 1000, 0, 600)
        self.setup_theme()
        self.set_buttons()
        self.clouds = arcade.SpriteList()
        self.decorations = arcade.SpriteList()

        self.scroll = 0
        self.curx = 0
        self.backdrop = arcade.SpriteList()
        self.backdrop.append(Backdrop(2))
        self.backdrop.append(Backdrop(1))
        self.backdrop.append(Backdrop(0))

        toAdd = Deco(arcade.load_texture("images/stupidInterface/dirt slope.png"), 1, 1870, 95)
        self.decorations.append(toAdd)

        for i in range(240):
            for y in range(4):
                toAdd = Deco(arcade.load_texture("images/stupidInterface/waveDirt.png"), 1, i * 16 - 50,
                             87 - 28 * y)
                self.decorations.append(toAdd)

        e = 0
        for i in range(30):
            toAdd = Deco(arcade.load_texture("images/stupidInterface/grass.png"), 1, e * 64 - 50, 100)
            self.decorations.append(toAdd)
            e += 1

        toAdd = Deco(arcade.load_texture("images/stupidInterface/grass slope.png"), 1, 1870, 110)
        self.decorations.append(toAdd)

        for i in range(30):
            toAdd = Deco(arcade.load_texture("images/stupidInterface/grass.png"), 1, e * 64 + 30, 100)
            self.decorations.append(toAdd)
            e += 1

        for i in range(5):  # TODO: clouds are glitchy when they're near the edge
            toAdd = Clouds(arcade.load_texture("images/stupidInterface/cloud.png"), 0.3, random.randint(-232, 1032),
                           random.randint(400, 600), random.uniform(-1, 1))
            while toAdd.direction == 0:
                toAdd.direction = random.uniform(-1, 1)
            self.clouds.append(toAdd)

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE)

    def set_buttons(self):
        self.theme.add_button_textures("images/stupidInterface/startButton.png", None,
                                       "images/stupidInterface/startButton.png", None)
        self.button_list.append(
            Start(self, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 320, 320, theme=self.theme))

        self.theme.add_button_textures("images/stupidInterface/backButton.png", None,
                                       "images/stupidInterface/backButton.png", None)
        self.button_list.append(BackButton(self, 2050, 500, 32, 32, theme=self.theme))

        self.theme.add_button_textures("images/stupidInterface/levelButton1.png",
                                       "images/stupidInterface/levelButton1.png",
                                       "images/stupidInterface/levelButton2.png")
        levelNum = 1
        for x in range(5):
            for y in range(2):
                self.button_list.append(LevelButton(self, SCREEN_WIDTH // 2 + 1750 + 100 * x,
                                        SCREEN_HEIGHT // 2 + 150 - 100 * y, 64, 64, theme=self.theme, levelNum=1))
                levelNum += 1

    def on_draw(self):
        arcade.start_render()

        self.backdrop.draw()
        self.clouds.draw()
        for i in self.button_list:
            i.draw()

        self.decorations.draw()

    def on_update(self, dt):
        if self.scroll > self.curx:
            for i in self.decorations:
                i.center_x = i.center_x - 20
            for i in self.button_list:
                i.center_x = i.center_x - 20
            self.curx += 20

        if self.scroll < self.curx:
            for i in self.decorations:
                i.center_x = i.center_x + 20
            for i in self.button_list:
                i.center_x = i.center_x + 20
            self.curx -= 20

        for i in self.clouds:  # move the clouds
            i.center_x += 0.2 * i.direction
            if (i.center_x > random.randint(832, 1032)) or (i.center_x < random.randint(-232, -32)):
                choice = random.randint(0, 1)
                if choice == 1:
                    i.center_x = random.randint(832, 1032)
                    i.center_y = random.randint(400, 600)
                    i.direction = -1
                if choice == 0:
                    i.center_x = random.randint(-232, -32)
                    i.center_y = random.randint(400, 600)
                    i.direction = 1


class GameOverView(arcade.View):
    def on_show(self):
        print('called onasdfasdf')
        arcade.set_viewport(0, 1000, 0, 600)
        arcade.set_background_color(arcade.color.BLACK)
        self.gameOverText = arcade.Sprite(center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 + 100)
        self.gameOverText.textures = [arcade.load_texture('images/stupidInterface/gameOverText.png')]
        self.gameOverText.texture = self.gameOverText.textures[0]
        self.setup_theme()
        self.set_buttons()

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE)

    def set_buttons(self):
        self.theme.add_button_textures("images/stupidInterface/restart.png", None,
                                       "images/stupidInterface/restart.png", None)
        self.button_list.append(RestartButton(self, theme=self.theme))

    def on_draw(self):
        arcade.start_render()

        self.gameOverText.draw()
        for i in self.button_list:
            i.draw()


class Deco(arcade.Sprite):
    def __init__(self, textures, scale, x, y):
        super().__init__()
        self.texture = textures
        self.scale = scale

        self.center_x = x
        self.center_y = y


class Backdrop(arcade.Sprite):
    def __init__(self, x):
        super().__init__()
        self.texture = arcade.load_texture("images/stupidInterface/menuBackground.png")
        self.scale = 1

        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2 + x * 100


class Clouds(arcade.Sprite):
    def __init__(self, textures, scale, x, y, orientation):
        super().__init__()
        self.direction = orientation
        self.texture = textures
        self.scale = scale

        self.center_x = x
        self.center_y = y


class Start(TextButton):
    def __init__(self, game, x=0, y=0, width=320, height=320, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game
        self.center_x = x
        self.pressed = False

    def on_press(self):
        if not self.pressed:
            self.pressed = True
            self.game.scroll = 2000

    def on_release(self):
        self.pressed = False


class BackButton(TextButton):
    def __init__(self, game, x=0, y=0, width=32, height=32, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game
        self.center_x = x
        self.pressed = False

    def on_press(self):
        if not self.pressed:
            self.pressed = True
            self.game.scroll = 0

    def on_release(self):
        self.pressed = False


class LevelButton(TextButton):
    def __init__(self, game, x=0, y=0, width=48, height=48, text="", theme=None, levelNum: int = None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game
        self.levelNum = levelNum

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.game.window.show_view(self.game.window.levels[self.levelNum])


class RestartButton(TextButton):
    def __init__(self, game, x=500, y=150, width=465, height=230, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game
        self.center_x, self.center_y = x, y
        self.pressed = False

    def on_press(self):
        if not self.pressed:
            self.pressed = True
            self.game.window.setup()
            self.game.window.show_view(self.game.window.menuView)

    def on_release(self):
        self.pressed = False
