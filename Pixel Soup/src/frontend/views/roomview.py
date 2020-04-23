import arcade


class RoomView(arcade.View):
    def __init__(self, option: str, username: str):
        super().__init__()
        self.option = option
        self.username = username

    def on_show(self) -> None:
        pass

    def on_draw(self) -> None:
        arcade.start_render()

    def setup(self) -> None:
        pass
