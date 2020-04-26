from pathlib import Path
from arcade.gui import *
import random
from gamer_gang.dumbConstants import *
from gamer_gang.epicAssets.baseLevelAndPhysics import Level


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
        self.totalTime = 0

        toAdd = Deco(arcade.load_texture(str(Path(__file__).parent) + "/images/dumbGUIImages/dirt slope.png"),
                     1, 1870, 95)
        self.decorations.append(toAdd)

        for i in range(240):
            for y in range(4):
                toAdd = Deco(arcade.load_texture(str(Path(__file__).parent) + "/images/dumbGUIImages/waveDirt.png")
                             , 1, i * 16 - 50, 87 - 28 * y)
                self.decorations.append(toAdd)

        e = 0
        for i in range(30):
            toAdd = Deco(arcade.load_texture(str(Path(__file__).parent) + "/images/dumbGUIImages/grass.png"), 1,
                         e * 64 - 50, 100)
            self.decorations.append(toAdd)
            e += 1

        toAdd = Deco(arcade.load_texture(str(Path(__file__).parent) + "/images/dumbGUIImages/grass slope.png"),
                     1, 1870, 110)
        self.decorations.append(toAdd)

        for i in range(30):
            toAdd = Deco(arcade.load_texture(str(Path(__file__).parent) + "/images/dumbGUIImages/grass.png"),
                         1, e * 64 + 30, 100)
            self.decorations.append(toAdd)
            e += 1

        for i in range(5):
            toAdd = Clouds(arcade.load_texture(str(Path(__file__).parent) + "/images/dumbGUIImages/cloud.png"),
                           0.3, random.randint(-232, 1032), random.randint(400, 600), random.uniform(-1, 1))
            while toAdd.direction == 0:
                toAdd.direction = random.uniform(-1, 1)
            self.clouds.append(toAdd)

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(32, arcade.color.WHITE, str(Path(__file__).parent) + "/pixelFont.TTF")

    def set_buttons(self):
        self.theme.add_button_textures(str(Path(__file__).parent) + "/images/dumbGUIImages/startButton.png", None,
                                       str(Path(__file__).parent) + "/images/dumbGUIImages/startButton.png", None)
        self.button_list.append(
            Start(self, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, 320, 320, theme=self.theme))

        self.theme.add_button_textures(str(Path(__file__).parent) + "/images/dumbGUIImages/backButton.png", None,
                                       str(Path(__file__).parent) + "/images/dumbGUIImages/backButton.png", None)
        self.button_list.append(BackButton(self, 2050, 500, 32, 32, theme=self.theme))

        self.theme.add_button_textures(str(Path(__file__).parent) + "/images/dumbGUIImages/levelButton1.png",
                                       str(Path(__file__).parent) + "/images/dumbGUIImages/levelButton1.png",
                                       str(Path(__file__).parent) + "/images/dumbGUIImages/levelButton2.png")
        levelNum = 1
        for y in range(2):
            for x in range(3):
                self.button_list.append(LevelButton(self, SCREEN_WIDTH//2 + 1930 + 100 * x,
                                                    SCREEN_HEIGHT//2 + 150 - 100 * y, 64, 64, text=str(levelNum),
                                                    theme=self.theme, levelNum=levelNum))
                levelNum += 1

    def on_draw(self):
        arcade.start_render()

        self.backdrop.draw()
        self.clouds.draw()
        for i in self.button_list:
            i.draw()

        self.decorations.draw()

    def on_update(self, dt):
        if self.totalTime == 0:
            self.window.sfx["menu music"].play(volume=0.5)
        if self.window.sfx["menu music"].get_length() < self.totalTime:
            self.totalTime = 0
        else:
            self.totalTime += dt

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
            if (i.center_x > SCREEN_WIDTH + i.width/2 and i.direction >0) or (i.center_x < i.width/2 and i.direction <=0):
                if random.randint(0,1) == 0:
                    i.center_x = random.randint(832, 1032)
                    i.center_y = random.randint(400, 600)
                    i.direction = random.randint(-100,1)/100
                else:
                    i.center_x = random.randint(-232, -32)
                    i.center_y = random.randint(400, 600)
                    i.direction = random.randint(1,100)/100


class GameOverView(arcade.View):
    def on_show(self):
        arcade.set_viewport(0, 1000, 0, 600)
        arcade.set_background_color(arcade.color.BLACK)
        self.gameOverText = arcade.Sprite(center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2 + 230)
        self.gameOverText.textures = [arcade.load_texture(str(Path(__file__).parent) +
                                                          '/images/dumbGUIImages/gameOverText.png')]
        self.gameOverText.texture = self.gameOverText.textures[0]
        self.setup_theme()
        self.set_buttons()

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE, str(Path(__file__).parent) + "/pixelFont.TTF")

    def set_buttons(self):
        self.theme.add_button_textures(str(Path(__file__).parent) + "/images/dumbGUIImages/backButton.png", None,
                                       str(Path(__file__).parent) + "/images/dumbGUIImages/backButton.png", None)
        self.button_list.append(BackToMenu(self, 100, 90, theme=self.theme))

        self.theme.add_button_textures(str(Path(__file__).parent) + "/images/dumbGUIImages/restart.png", None,
                                       str(Path(__file__).parent) + "/images/dumbGUIImages/restart.png", None)
        self.button_list.append(RestartButton(self, theme=self.theme))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f'you died from: {self.window.deathCause}',
                         SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 50, arcade.color.WHITE,
                         font_name=str(Path(__file__).parent) + "/pixelFont.TTF", font_size=22, align='center')
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
        self.texture = arcade.load_texture(str(Path(__file__).parent) + "/images/dumbGUIImages/menuBackground.png")
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
            self.game.window.sfx['menu music'].stop()
            self.game.window.currLevel = self.levelNum
            self.game.window.show_view(self.game.window.levels[self.levelNum])


class RestartButton(TextButton):
    def __init__(self, game, x=500, y=120, width=310, height=153.33333, text="", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game
        self.center_x, self.center_y = x, y
        self.pressed = False

    def on_press(self):
        if not self.pressed:
            self.pressed = True
            self.game.window.setup()
            self.game.window.show_view(self.game.window.levels[self.game.window.currLevel])

    def on_release(self):
        self.pressed = False

class BackToMenu(TextButton):
    def __init__(self, game, x=0, y=0, width=128, height=128, font_size=6, text="menu", theme=None):
        super().__init__(x, y, width, height, font_size=font_size, text=text, theme=theme)
        self.game = game
        self.center_x = x
        self.pressed = False

    def on_press(self):
        if not self.pressed:
            self.game.window.setup()  # setup does have the show_view in it so yea
        self.pressed = True
