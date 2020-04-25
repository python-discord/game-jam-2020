import arcade
from main import *


class Main:
    def __init__(self):
        self.settings = Settings(self)
        self.menu = MainMenu(self)
        self.song_selection = SongSelection(self)
        self.window = arcade.Window(
            #self.menu.width,
            #self.menu.height,
            1000,
            600,
            title="3 Strings",
            fullscreen=False, update_rate=1/64)
        self.play_screen = GameScreen(self)

    @property
    def brightness(self):
        return self.settings.brightness

    @property
    def volume(self):
        return self.settings.volume


if __name__ == "__main__":
    main = Main()
    main.window.show_view(main.play_screen)
    main.play_screen.setup({'name': 'undertale', 'path': 'track_1', 'type': 'wav'})
    arcade.run()

