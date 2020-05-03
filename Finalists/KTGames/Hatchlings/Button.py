# GUI package
import arcade

class Button:
    """ Text based, put under the images, excluding actual text as icon above will speak for function of the button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 face_color=arcade.color.BLUE_VIOLET,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):

        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        # draw the actual GUI of the button

        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.face_color)

        # if the button is pressed, make it the highlught color, if it isn't, make it the shadow color
        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # bottom horizontal line under button
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


# Check buttons for clicks
def check_mouse_press_for_buttons(x, y, button_list):
    # Given an x, y, see if we need to register any button clicks
    # if logic checks to see if click is outside of button space, has function continue unless it is a hit
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()

# Check button for release, which ultimately will trigger event
def check_mouse_release_for_buttons(_x, _y, button_list):
    # if a mouse button has been released, see if we need to process any release events
    for button in button_list:
        if button.pressed:
            button.on_release()


""" TODO: subclass button to link to event for each of the eight icons """

class IconButton(Button):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 40, 10)
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class TextButton(Button):
    def __init__(self, center_x, center_y, action_function, text, font_size=16, face_color=arcade.color.BLUE_VIOLET):
        super().__init__(center_x, center_y, 80, 40)
        self.action_function = action_function

        # self.text = text
        # self.font_size = font_size
        self.face_color = face_color

    def on_release(self):
        # calling existing function
        super().on_release()
        # adding
        self.action_function()

    def draw(self):
        super().draw()









