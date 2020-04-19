import arcade
from screeninfo import get_monitors


class Settings(arcade.View):

    width = get_monitors()[0].width
    height = get_monitors()[0].height

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color([0, 0, 0])
        arcade.draw_text("SETTINGS", self.width*0.3, self.height*0.8,
                         [255, 255, 255], min(self.width, self.height)/8,
                         align="center", width=int(self.width*0.4))
