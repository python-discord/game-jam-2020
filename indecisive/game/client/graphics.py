import arcade


class Display(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Three of a king")
        self.title = arcade.sprite_list
        arcade.set_background_color((255, 255, 255))
        self.sceen_time = 0  # used for animations
        self.scene = "title"
        self.scene_spritelists = dict()

    def setup(self):
        self.scene_spritelists["title"] = arcade.SpriteList()
        self.scene_spritelists["title"].extend([
            arcade.Sprite(
                "./assets/title.png",
                scale=0.5,
                center_x=640,
                center_y=360
            ),
            arcade.Sprite(
                "./assets/Adith.png",
                scale=0.15,
                center_x=640,
                center_y=300
            ),
            arcade.Sprite(
                "./assets/TheLordOfTartarus.png",
                scale=0.15,
                center_x=640,
                center_y=260
            ),
            arcade.Sprite(
                "./assets/xedre.png",
                scale=0.15,
                center_x=640,
                center_y=220
            )
        ])

    def on_draw(self):

        arcade.start_render()
        if self.scene == "title":
            self.scene_spritelists["title"].draw()
        else:
            alpha = 255 - int(self.scene_frame//1.75)
            if alpha < 0:
                alpha = 0
            arcade.draw_text("Indecisive", 0, 360, (0, 0, 0, alpha), font_size=50, align="center", width=1280)
            if self.hide != 0:
                self.hide -= 0.5

    def on_update(self, delta_time: float):
        if self.scene == "title":
            self.sceen_time += delta_time
            fade = 255 - (self.sceen_time - 2) * 100
            if fade < 0:
                fade = 0
            elif fade > 255:
                fade = 255
            for x in self.scene_spritelists["title"]:
                x.alpha = fade
            if self.sceen_time < 2:
                fade_in = (self.sceen_time - 0.5) * 200
                if fade_in < 0:
                    fade_in = 0
                elif fade_in > 255:
                    fade_in = 255
                for x in self.scene_spritelists["title"][1:]:
                    x.alpha = fade_in


def main():
    display1 = Display()
    display1.setup()
    arcade.run()
