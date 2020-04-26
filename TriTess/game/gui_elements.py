from arcade.gui import TextButton

from TriTess.game.trigrid import TriGrid


class PlayHex2Btn(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text="2 Player", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.game.game_type = "hex2"
            self.game.trigrid = TriGrid(self.game.width,  self.game.height, self.game.game_type)
            self.pressed = False
            self.game.on_draw()


class PlayTri3Btn(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text="3 Player", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.game.game_type = "tri3"
            self.game.trigrid = TriGrid(self.game.width,  self.game.height, self.game.game_type)
            self.pressed = False
            self.game.on_draw()


class SkipTurnBtn(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text="Skip Turn", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            player_name = self.game.trigrid.next_player()
            self.game.display_text(f"{player_name}'s turn")
            self.pressed = False
