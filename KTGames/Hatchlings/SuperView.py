# imports and settings
import arcade

from Button import Button, check_mouse_press_for_buttons, check_mouse_release_for_buttons, \
    IconButton, TextButton
from PetCharacter import PetCharacter

""" CONSTANTS """
# screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TITLE = "Virtual Pet"

# background color
BACKGROUND_COLOR = arcade.color.BLUE_VIOLET

# select menu items
EAT_PATH = r"./Sprites/select_menu_options/eat.png"
LIGHT_PATH = r"./Sprites/select_menu_options/lightbulb.png"
GAME_PATH = r"./Sprites/select_menu_options/game.png"
SICK_CARE_PATH = r"./Sprites/select_menu_options/medicine.png"
BATHROOM_PATH = r"./Sprites/select_menu_options/duck.png"
HEALTH_PATH = r"./Sprites/select_menu_options/scale.png"
DISCIPLINE_PATH = r"./Sprites/select_menu_options/discipline.png"
ATTENTION_PATH = r"./Sprites/select_menu_options/attention.png"

# menu scaling
MENU_ITEM_SCALING = 1.8
FOOD_SCALING = .5
EMOTION_SCALING = 3
HEALTH_SCREEN_SCALE = 2

# button text
START_TEXT = r"./Sprites/Buttons/Start.png"
RESET_TEXT = r"./Sprites/Buttons/Reset.png"
HOME_TEXT = r"./Sprites/Buttons/Home.png"
START_SCALING = 1.8
RESET_SCALING = 1.5
HOME_SCALING = 1.7

class SuperView(arcade.View):

    def __init__(self):
        super().__init__()

        self.pet = None

        """ Sprite lists """
        # list for option buttons
        self.button_list = []

        # 4.24 text sprites for buttons, draw_text takes up too much memory
        self.button_text_list = arcade.SpriteList(is_static=True)

        self.home_text = arcade.Sprite(HOME_TEXT, HOME_SCALING)
        self.home_text.center_x = 85
        self.home_text.center_y = 440

        self.reset_text = arcade.Sprite(RESET_TEXT, RESET_SCALING)
        self.reset_text.center_x = 165
        self.reset_text.center_y = 57

        self.start_text = arcade.Sprite(START_TEXT, START_SCALING)
        self.start_text.center_x = 65
        self.start_text.center_y = 60

        self.button_text_list.append(self.home_text)
        self.button_text_list.append(self.reset_text)
        self.button_text_list.append(self.start_text)

        """ Sprites """

        """ 8 Option sprites """
        # select menu options
        self.select_menu_options = arcade.SpriteList(is_static=True)

        """ top half of screen """
        self.eat_option = arcade.Sprite(EAT_PATH, MENU_ITEM_SCALING)
        self.eat_option.center_x = 60
        self.eat_option.center_y = 535

        self.light_option = arcade.Sprite(LIGHT_PATH, MENU_ITEM_SCALING)
        self.light_option.center_x = 195
        self.light_option.center_y = 535

        self.game_option = arcade.Sprite(GAME_PATH, MENU_ITEM_SCALING)
        self.game_option.center_x = 350
        self.game_option.center_y = 535

        self.sick_care_option = arcade.Sprite(SICK_CARE_PATH, MENU_ITEM_SCALING)
        self.sick_care_option.center_x = 505
        self.sick_care_option.center_y = 535

        """ bottom half of screen """
        self.bathroom_option = arcade.Sprite(BATHROOM_PATH, MENU_ITEM_SCALING)
        self.bathroom_option.center_x = 60
        self.bathroom_option.center_y = 160

        self.health_option = arcade.Sprite(HEALTH_PATH, MENU_ITEM_SCALING)
        self.health_option.center_x = 195
        self.health_option.center_y = 160

        self.discipline_option = arcade.Sprite(DISCIPLINE_PATH, MENU_ITEM_SCALING)
        self.discipline_option.center_x = 350
        self.discipline_option.center_y = 160

        self.attention_option = arcade.Sprite(ATTENTION_PATH, MENU_ITEM_SCALING)
        self.attention_option.center_x = 505
        self.attention_option.center_y = 160

        # Append all menu items to test scaling/drawing for now, will remove later with select functionality
        self.select_menu_options.append(self.eat_option)
        self.select_menu_options.append(self.light_option)
        self.select_menu_options.append(self.game_option)

        self.select_menu_options.append(self.sick_care_option)
        self.select_menu_options.append(self.bathroom_option)
        self.select_menu_options.append(self.health_option)

        self.select_menu_options.append(self.discipline_option)
        self.select_menu_options.append(self.attention_option)

        """ Icon buttons that go under the menu option sprites"""

        # top half
        eat_button = IconButton(60, 500, self.hit_eat)
        self.button_list.append(eat_button)

        light_button = IconButton(195, 500, self.hit_light)
        self.button_list.append(light_button)

        game_button = IconButton(350, 500, self.hit_game)
        self.button_list.append(game_button)

        medicine_button = IconButton(505, 500, self.hit_medicine)
        self.button_list.append(medicine_button)

        # bottom half
        flush_button = IconButton(60, 120, self.hit_flush)
        self.button_list.append(flush_button)

        scale_button = IconButton(195, 120, self.hit_health_stats)
        self.button_list.append(scale_button)

        discipline_button = IconButton(350, 120, self.hit_discipline)
        self.button_list.append(discipline_button)

        attention_button = IconButton(505, 120, self.hit_attention)
        self.button_list.append(attention_button)

        # start, home and reset button
        home_button = TextButton(85, 440, self.hit_home, "Home")
        self.button_list.append(home_button)

        start_button = TextButton(65, 60, self.hit_start, "START", face_color=arcade.color.GO_GREEN)
        self.button_list.append(start_button)

        reset_button = TextButton(165, 60, self.hit_reset, "RESET", face_color=arcade.color.BRICK_RED)
        self.button_list.append(reset_button)

        # UPDATE 4.22 -  shape list for main panels to improve efficiency
        self.screen_shape_list = None

    def setup(self):
        screen_panel = arcade.create_rectangle_filled(center_x=300, center_y=350, width=550, height=450,
                                                      color=arcade.color.ASH_GREY)
        top_option_panel = arcade.create_rectangle_filled(center_x=300, center_y=530, width=550, height=95,
                                                          color=arcade.color.AUROMETALSAURUS)
        bottom_option_panel = arcade.create_rectangle_filled(center_x=300, center_y=150, width=550, height=95,
                                                             color=arcade.color.AUROMETALSAURUS)

        self.screen_shape_list = arcade.ShapeElementList()
        self.screen_shape_list.append(screen_panel)
        self.screen_shape_list.append(top_option_panel)
        self.screen_shape_list.append(bottom_option_panel)

    def on_show(self):
        # Blue violet base
        arcade.set_background_color(BACKGROUND_COLOR)


    def on_draw(self):

        """ Base panels """
        # get ready to draw
        arcade.start_render()

        # main screen
        self.screen_shape_list.draw()

        """ Main Button List """
        for button in self.button_list:
            button.draw()

        """ Button Text """
        self.button_text_list.draw()

        """ 8 Menu Option Sprites """
        self.select_menu_options.draw()

    """ CONTROLS - check for button interactions to hit menu items """

    def on_mouse_press(self, x, y, button, key_modifiers):
        # called when the user presses a mouse button
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        # called on button release
        check_mouse_release_for_buttons(x, y, self.button_list)

    """ 
    Methods for buttons in game (eight options) logic that apply to each derived class 
    or declaration so button in main screen draw can be bound to method to be used in derived classes
    """

    def hit_home(self):
        print("hit home")

    def hit_start(self):
        print("hit start")

    def hit_reset(self):
        print("hit reset")

    def hit_light(self):
        print("hit light")

    def hit_game(self):
        print("hit game")

    def hit_medicine(self):
        print("hit medicine")

    def hit_flush(self):
        print("hit flush")

    def hit_health_stats(self):
        print("hit health stats")

    def hit_discipline(self):
        print("hit discipline")

    def hit_attention(self):
        print("hit attention")

    def hit_eat(self):
        print("hit eat")


