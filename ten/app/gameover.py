import arcade
from buttons import MenuButton
from gamescreen import GameView


class GameoverView(arcade.View):
    def __init__(self):
        super().__init__()
        print("GameoverView Created")
        self.theme = None

    def setup(self):
        pass

    def setup_buttons(self):
        from menuscreen import MenuView

        go_back = MenuButton(
            self,
            GameView(),
            int(self.window.WINDOW_WIDTH / 2),
            int(self.window.WINDOW_HEIGHT / 3),
            200,
            100,
            "Retry",
            theme=self.theme,
        )
        self.button_list.append(go_back)

    def on_show(self):
        self.setup_buttons()
        arcade.set_background_color(arcade.color.RED)

    def update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
