import arcade
from arcade.gui import Theme
import string
import random

from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT

from .settingsview import SettingsView
from .roomview import RoomView


class NewRoomButton(arcade.TextButton):
    def __init__(
        self,
        view_reference,
        dialoguebox,
        x=0,
        y=0,
        width=100,
        height=40,
        text="New Room",
        theme=None,
    ):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view_reference = view_reference
        self.dialoguebox = dialoguebox

    def on_press(self) -> None:
        if not self.dialoguebox.active:
            self.pressed = True

    def on_release(self) -> None:
        if self.pressed:
            self.dialoguebox.active = True


class JoinRoomButton(arcade.TextButton):
    def __init__(
        self,
        view_reference,
        dialoguebox,
        x=0,
        y=0,
        width=100,
        height=40,
        text="Join Room",
        theme=None,
    ):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view_reference = view_reference
        self.dialoguebox = dialoguebox

    def on_press(self) -> None:
        if not self.dialoguebox.active:
            self.pressed = True

    def on_release(self) -> None:
        if self.pressed:
            self.dialoguebox.active = True


class ContinueButton(arcade.TextButton):
    def __init__(
        self,
        view_reference,
        dialoguebox,
        x=0,
        y=0,
        width=110,
        height=50,
        text="Continue",
        theme=None,
    ):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view_reference = view_reference
        self.dialoguebox = dialoguebox

    def on_press(self) -> None:
        if self.dialoguebox.active:
            self.pressed = True

    def on_release(self) -> None:
        if self.pressed and self.dialoguebox.active:
            room_name = self.view_reference.text_form.text_storage.text
            self.pressed = False

            if not room_name:
                return

            if self.view_reference.window.button_list[0].pressed:
                action = "create"
            elif self.view_reference.window.button_list[1].pressed:
                action = "join"

            username = random.randint(100000, 999999)

            self.view_reference.window.dialogue_box_list = []
            self.view_reference.clear_buttons()

            room_view = RoomView(self.view_reference, room_name, username, mode=action)
            room_view.setup()
            self.view_reference.window.show_view(room_view)


class SettingsButton(arcade.TextButton):
    def __init__(
        self,
        view_reference,
        x=0,
        y=0,
        width=100,
        height=40,
        text="Settings",
        theme=None,
    ):
        super().__init__(x, y, width, height, text, theme=theme)
        self.view_reference = view_reference

    def on_press(self) -> None:
        if not self.view_reference.window.dialogue_box_list[0].active:
            self.pressed = True

    def on_release(self) -> None:
        if self.pressed and not self.view_reference.window.dialogue_box_list[0].active:
            self.view_reference.clear_buttons()

            settings_view = SettingsView()
            settings_view.setup()
            self.view_reference.show_view(settings_view)


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.theme = None
        self.half_width = SCREEN_WIDTH / 2
        self.half_height = SCREEN_HEIGHT / 2

    def on_show(self) -> None:
        pass

    def on_draw(self) -> None:
        arcade.start_render()

    def setup_dialogue_box(self) -> None:
        color = (220, 228, 255)
        dialoguebox = arcade.DialogueBox(
            self.half_width,
            self.half_height,
            self.half_width * 1.1,
            self.half_height * 1.5,
            color,
            self.theme,
        )
        continue_button = ContinueButton(
            self,
            dialoguebox,
            self.half_width,
            self.half_height - (self.half_height / 2) + 40,
            int(SCREEN_WIDTH * 0.2),
            theme=self.theme,
        )
        dialoguebox.button_list.append(continue_button)

        hint_text = arcade.draw_text(
            "Room Name",
            self.half_width * 0.85,
            self.half_height + 30,
            arcade.csscolor.BLACK,
            18,
        )

        dialoguebox.text_list.append(hint_text)

        self.text_form = arcade.TextBox(
            self.half_width, self.half_height, theme=self.theme,
        )

        dialoguebox.text_list.append(self.text_form)

        self.window.dialogue_box_list.append(dialoguebox)

    def set_dialogue_box_texture(self) -> None:
        dialogue_box = ":resources:gui_themes/Fantasy/DialogueBox/DialogueBox.png"
        self.theme.add_dialogue_box_texture(dialogue_box)

    def set_button_textures(self) -> None:
        """Give the same style to all the buttons using self.theme."""
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self) -> None:
        """Create a theme to be used by the Main Menu buttons."""
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.BLACK)

        self.set_dialogue_box_texture()
        self.set_button_textures()

    def set_buttons(self) -> None:
        """Initialize all the Main Menu buttons."""
        self.window.button_list.append(
            NewRoomButton(
                self,
                self.window.dialogue_box_list[0],
                0.5 * SCREEN_WIDTH,
                0.62 * SCREEN_HEIGHT,
                int(0.3 * SCREEN_WIDTH),
                int(0.1 * SCREEN_HEIGHT),
                theme=self.theme,
            )
        )

        self.window.button_list.append(
            JoinRoomButton(
                self,
                self.window.dialogue_box_list[0],
                0.5 * SCREEN_WIDTH,
                0.5 * SCREEN_HEIGHT,
                int(0.3 * SCREEN_WIDTH),
                int(0.1 * SCREEN_HEIGHT),
                theme=self.theme,
            )
        )

        self.window.button_list.append(
            SettingsButton(
                self,
                0.5 * SCREEN_WIDTH,
                0.38 * SCREEN_HEIGHT,
                int(0.3 * SCREEN_WIDTH),
                int(0.1 * SCREEN_HEIGHT),
                theme=self.theme,
            )
        )

    def clear_buttons(self) -> None:
        """
        Used to remove all the buttons in Main Menu while switching to
        another view.
        """
        self.window.button_list = []

    def setup(self) -> None:
        """Initialize the menu."""
        self.setup_theme()
        self.setup_dialogue_box()
        self.set_buttons()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if self.window.dialogue_box_list[0].active:
            self.change_text(self.text_form, key, modifiers)

    def change_text(
        self, textbox: arcade.TextBox, key: int, modifiers: int, limit: int = 16
    ) -> None:
        """Catch key events and show the letters in a specified TextBox."""
        if key == arcade.key.BACKSPACE:
            textbox.text_storage.text = (
                textbox.text_display.text
            ) = textbox.text_storage.text[:-1]
        elif 97 <= key <= 122:
            if len(textbox.text_display.text) >= limit:
                return

            if modifiers & 1 == 1 or modifiers & 8 == 8:
                alphabet = string.ascii_uppercase
            else:
                alphabet = string.ascii_lowercase

            new_text = textbox.text_storage.text + alphabet[key - 97]
            textbox.text_storage.text = textbox.text_display.text = new_text
