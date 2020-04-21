from arcade import *
import arcade


class MenuButton(TextButton):
    def __init__(self, current_view, next_view, x, y, width, height, text, theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.next_view = next_view
        self.current_view = current_view

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.next_view.theme = self.theme
            self.current_view.window.show_view(self.next_view)
            self.next_view.setup()


class QuitButton(TextButton):
    def __init__(self, x, y, width, height, text, theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            arcade.close_window()
