import arcade
from pyglet.input.base import Joystick

from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_PATH
from .mainmenuview import MainMenuView

from textwrap import dedent

DATA_PATH = f"{GAME_PATH}/data"


class MainView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.music = arcade.load_sound(f"{DATA_PATH}/music.wav")
        self.music.play(volume=0.2)

        self.half_width = SCREEN_WIDTH / 2
        self.half_height = SCREEN_HEIGHT / 2

        self.theme = None

    def on_show(self) -> None:
        """Called when MainView should draw."""
        if self.window.joystick:
            self.window.joystick.set_handler(
                "on_joybutton_release", self.on_joybutton_release
            )

    def on_draw(self) -> None:
        """Show the widgets."""
        arcade.start_render()

        # Draw the background
        arcade.draw_lrwh_rectangle_textured(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background
        )

        arcade.draw_text(
            self.window.caption,
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
        )

        arcade.draw_text(
            "Press S to start | Toggle instructions with I",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
        )

    def add_dialogue_box(self):
        color = (220, 228, 255)
        dialoguebox = arcade.gui.DialogueBox(
            self.half_width,
            self.half_height,
            self.half_width * 1.1,
            self.half_height * 1.5,
            color,
            self.theme,
        )
        message = dedent(
            """
        W | Space: jump
        A | Left Arrow: move to the left
        S | Right Arrow: move to the right
        """
        )
        dialoguebox.text_list.append(
            arcade.draw_text(
                message,
                SCREEN_WIDTH * 0.3,
                SCREEN_HEIGHT * 0.4,
                self.theme.font_color,
                self.theme.font_size,
            )
        )
        self.window.dialogue_box_list.append(dialoguebox)

    def set_dialogue_box_texture(self):
        dialogue_box = ":resources:gui_themes/Fantasy/DialogueBox/DialogueBox.png"
        self.theme.add_dialogue_box_texture(dialogue_box)

    def set_theme(self):
        self.theme = arcade.gui.Theme()
        self.set_dialogue_box_texture()
        self.theme.set_font(20, arcade.color.BLACK)

    def setup(self) -> None:
        """Setup the view and initialize the variables."""
        self.background = arcade.load_texture(f"{DATA_PATH}/bg.gif")
        self.set_theme()
        self.add_dialogue_box()

    def _to_main_menu(self) -> None:
        """Switch to the Main Menu View."""
        main_menu_view = MainMenuView()
        self.window.show_view(main_menu_view)
        main_menu_view.setup()

        if self.window.joystick:
            self.window.joystick.remove_handler(
                "on_joybutton_release", self.on_joybutton_release
            )

    def _toggle_instructions(self) -> None:
        """Open/Close a DialogueBox with the Instructions."""
        self.window.dialogue_box_list[0].active = not self.window.dialogue_box_list[
            0
        ].active

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Move to the next view if S is pressed, or move to the instructions
        if I is pressed.
        """
        if key == arcade.key.S and not self.window.dialogue_box_list[0].active:
            self._to_main_menu()
        elif key == arcade.key.I:
            self._toggle_instructions()

    def on_joybutton_release(self, joystick: Joystick, button: int) -> None:
        """Move to the next view when any joystick button is pressed."""
        self._to_main_menu()
