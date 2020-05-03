import arcade


class SimpleButton(arcade.TextButton):
    def __init__(self, action, text="", x=0, y=0, width=100, height=40,
                 font_size=18, font="Arial", font_color=(255, 255, 255),
                 face_color=(50, 50, 50), highlight_color=(75, 75, 75), shadow_color=(150, 150, 150),
                 theme=None):
        super().__init__(
            x, y, width, height, text,
            font_size, font, font_color,
            face_color, highlight_color, shadow_color,
            theme=theme
        )
        self.action = action

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.action()
            self.pressed = False
