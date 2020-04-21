import arcade

class Options():
    def __init__(self):
        self.spritelist = arcade.SpriteList()
        self.buttonlist = arcade.View.button_list()
        self.spritedict = dict()
        self.timeAlive = 0
        self.sprite_setup()
        self.button_setup()
        arcade.set_background_color(arcade.color.BEAU_BLUE)
        self.background = arcade.load_textures()
        normal = "./assets/normal_Button.png"
        hover = "./assets/Hovered_Button.png"
        clicked = "./assets/Hovered_Button.png"
        self.theme.add_button_textures(normal, hover, clicked)

    def sprite_setup(self):
        self.spritedict = {
            "back": arcade.Sprite(
                "./assets/Options.png",
                scale=0.25,
                center_x=160,
                center_y=687.5
            )
        }
        self.spritelist.extend(self.spritedict.values())

    def button_setup(self):
        esc = Button("options", "main_menu", 560, 620, 400, 150, "Exit", self.theme)
        music = Button("options", "option", 600, 400, "Music", self.theme)
        accept = Button("options", "main_menu", 500, 200, "Accept", self.theme)
        button_items = [esc, music, accept]
        self.buttonlist += button_items

    def update(self, delta_time: float) -> None:
        self.timeAlive += delta_time

    def draw(self):
        self.spritelist.draw()


class Button(arcade.TextButton):
    def __init__(self, start_scene, next_scene, x, y, width, height, text, theme=None):
        super.__init__(x, y, width, height, text, theme=theme, font="Roboto", font_color=255)
        self.start_scene = start_scene
        self.next_scene = next_scene
        self.clicked = False

    def on_press(self):
        self.clicked = True

    def on_release(self):
        if self.clicked:
            if self.next_scene == "Exit":
                arcade.close_window()
            else:
                self.display.change_scenes(self.next_scene)
