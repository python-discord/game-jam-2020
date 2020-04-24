import arcade

from triple_vision import Settings as s
from triple_vision.text_input import TextInput


class PasswordTextInput(TextInput):

    def __init__(self, view, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.view = view

    def on_enter(self, text) -> None:
        self.view.login(text)


class MainMenu(arcade.View):

    def __init__(self) -> None:
        super().__init__()

        self.username = TextInput(
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 + 40,
            border_width=3
        )
        self.password = PasswordTextInput(
            self,
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 - 40,
            border_width=3
        )

        arcade.set_background_color(arcade.csscolor.MAROON)

    def login(self, password) -> None:
        print(self.username.text, password)

    def setup(self) -> None:
        pass

    def on_key_press(self, key, modifiers) -> None:
        self.username.process_key_press(key, modifiers)
        self.password.process_key_press(key, modifiers)

    def on_mouse_press(self, x, y, key, modifiers) -> None:
        self.username.process_mouse_press(x, y, key, modifiers)
        self.password.process_mouse_press(x, y, key, modifiers)

    def on_draw(self) -> None:
        arcade.start_render()

        self.username.draw()
        self.password.draw()

    def on_update(self, delta_time: float = 1/60) -> None:
        self.username.on_update(delta_time)
        self.password.on_update(delta_time)
