# imports and settings
import arcade
import random
from SuperView import SuperView
from PetCharacter import PetCharacter

from Button import Button, check_mouse_press_for_buttons, check_mouse_release_for_buttons,\
    IconButton, TextButton


""" CONSTANTS"""
# screen setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# SPLASH SCREEN
SPLASH_SCREEN = r"./Sprites/SplashScreen.png"
SPLASH_SCREEN_SCALE = 3.0

# SOUND EFFECT FILES
ATTENTION_SOUND_FILE = "./Sound/HatchlingWaste.wav"

# EAT VIEW
FOOD_IMG = "./Animation/FoodGameAndStats/Burger.png"
FOOD_SCALE = 2.0

# FULL VIEW
FULL_EX = "./Animation/FoodGameAndStats/wont_eat.png"
FULL_SCALE = 3.0

# DARK VIEW
SLEEPING = r"./Animation/FoodGameAndStats/ZSleep.png"
SLEEPING_SCALE = 3.0

# GAME VIEW
GAME_IMG = "./Animation/FoodGameAndStats/GameController32.png"
GAME_SCALE = 2.0

# EMOTIONS
HEART_IMG = "./Animation/FoodGameAndStats/hidefheart.png"
HEART_SCALE = .7

# STATS SCREEN
BLANK_HEART = "./Animation/FoodGameAndStats/hidefheart_blank.png"
BLANK_HEART_SCALE = .7

# TEXT FOR STATS
MOOD_TEXT = r"./Sprites/Buttons/Mood.png"
HUNGER_TEXT = r"./Sprites/Buttons/Hunger.png"
STAT_TEXT_SCALING = 1.5

# MOOD
MOOD_UNHAPPY = "./Animation/FoodGameAndStats/mood_unhappy.png"
MOOD_OK = "./Animation/FoodGameAndStats/mood_ok.png"
MOOD_NEUTRAL = "./Animation/FoodGameAndStats/mood_neutral.png"
MOOD_HAPPY = "./Animation/FoodGameAndStats/mood_happy.png"
MOOD_SCALE = 3.0

# WASTE
POOP = r"./Sprites/select_menu_options/poop.png"
POOP_SCALE = 2

# GAME OVER
GAME_OVER = "./Animation/GameOver/GAMEOVER.png"
GAME_OVER_SCALE = 5.0


# planet
PLANET = "./Animation/GameOver/Saturn.png"
PLANET_SCALE = 4.0



class MainView(SuperView):

    def __init__(self, game_start=False, pet_object=None):
        super().__init__()
        self.pet_list = None
        self.pet = pet_object

        self.waste_list = None

        # logic on whether or not the player has clicked start to begin the game
        # adjusts the draw method for the Sprite
        self.game_start = game_start
        self.light_off = False
        self.splash_screen_spritelist = None
        self.attention_sound = arcade.load_sound(ATTENTION_SOUND_FILE)


    def setup(self):
        super().setup()
        if self.pet is None:
            self.pet = PetCharacter()

        self.pet_list = arcade.SpriteList()
        self.pet_list.append(self.pet)

        self.splash_screen_spritelist = arcade.SpriteList(is_static=True)
        self.splash_screen = arcade.Sprite(SPLASH_SCREEN, SPLASH_SCREEN_SCALE)
        self.splash_screen.center_x = 300
        self.splash_screen.center_y = 300
        self.splash_screen_spritelist.append(self.splash_screen)

        # waste
        self.waste_list = arcade.SpriteList()

    def on_show(self):
        super().on_show()

    def on_draw(self):
        super().on_draw()

        """ The Pet """
        if self.game_start:
            self.pet_list.draw()
        elif self.game_start is False:
            self.splash_screen_spritelist.draw()

        if self.pet.waste:
            poop = arcade.Sprite(POOP, POOP_SCALE)
            poop.center_x = 150
            poop.center_y = 270
            self.waste_list.append(poop)
            self.waste_list.draw()

        if self.pet.needs_attention:
            arcade.draw_rectangle_outline(505, 160, 75, 50, arcade.color.RED)


    def on_update(self, delta_time):
        """ Animation """
        # animation
        self.pet_list.update_animation()

        # time
        self.pet.total_time += delta_time

        minutes = int(self.pet.total_time) // 60

        """ Age/Time Lapse Logic """
        if minutes <= 1:
            self.pet.age = 1

        elif 1 < minutes <= 2:
            self.pet.age = 2
            if self.pet.hunger_meter > 0:
                self.pet.hunger_meter -= 1
            if self.pet.mood_meter > 2:
                self.pet.mood_meter -= 1

        elif 2 < minutes <= 3:
            self.pet.age = 3

        elif 3 < minutes <= 4:
            self.pet.age = 4
            if self.pet.hunger_meter > 0:
                self.pet.hunger_meter -= 1
            if self.pet.mood_meter > 2:
                self.pet.mood_meter -= 1

        elif 4 < minutes <= 5:
            self.pet.age = 5

        elif 5 < minutes <= 6:
            self.pet.age = 6
            if self.pet.hunger_meter > 0:
                self.pet.hunger_meter -= 1
            if self.pet.mood_meter > 2:
                self.pet.mood_meter -= 1

        elif 6 < minutes <= 7:
            self.pet.age = 7

        elif 7 < minutes <= 8:
            self.pet.age = 8
            if self.pet.hunger_meter > 0:
                self.pet.hunger_meter -= 1
            if self.pet.mood_meter > 2:
                self.pet.mood_meter -= 1

        elif 8 < minutes <= 9:
            self.pet.age = 9

        elif 9 < minutes <= 10:
            self.pet.age = 10

        else:
            # die from natural causes
            self.game_start = False
            game_over_view = GameOverView(self.pet)
            game_over_view.setup()
            self.window.show_view(game_over_view)

        """ Waste/Sickness Logic """
        rand_int = random.randrange(0, 81)

        # baby
        if 1 < minutes <= 2:
            if rand_int == 5:
                self.pet.sick = True
                self.pet.needs_attention = True
            elif rand_int == 9:
                self.pet.waste = True
                self.pet.needs_attention = True
            elif rand_int == 11:
                self.pet.needs_attention = True

        # toddler
        if 4 < minutes <= 5:
            if rand_int == 7:
                self.pet.sick = True
                self.pet.needs_attention = True
            elif rand_int == 19:
                self.pet.waste = True
                self.pet.needs_attention = True
            elif rand_int == 2:
                self.pet.needs_attention = True

        # kid/young adult sea creature
        if 6 < minutes <= 7:
            if rand_int == 3:
                self.pet.sick = True
                self.pet.needs_attention = True
            elif rand_int == 4:
                self.pet.waste = True
                self.pet.needs_attention = True
            elif rand_int == 17:
                self.pet.needs_attention = True


    """ Main Game Loop Logic"""
    def hit_start(self):
        self.game_start = True


    def hit_reset(self):
        main_view = MainView()
        main_view.setup()
        self.window.show_view(main_view)

    def hit_eat(self):
        if self.game_start:
            self.pet.is_eating = True

            if self.pet.hunger_meter <= 4:
                self.pet.care_score += 1
                self.pet.hunger_meter += 1

            if self.pet.hunger_meter <= 4:
                eat_view = EatView(self.pet)
                eat_view.setup()
                self.window.show_view(eat_view)

            elif self.pet.hunger_meter > 4:
                full_view = FullView(self.pet)
                full_view.setup()
                self.window.show_view(full_view)


    def hit_light(self):
        if self.game_start:
            if self.light_off is False:
                self.light_off = True
                self.pet.care_score += 1
                dark_view = DarkView(self.pet)
                dark_view.setup()
                self.window.show_view(dark_view)

    def hit_game(self):
        if self.game_start:

            # making sure the mood meter cannot exceed 4 to increase challenge
            if self.pet.mood_meter < 4:
                self.pet.mood_meter += 1
                self.pet.care_score += 1

            game_view = GameView(self.pet)
            game_view.setup()
            self.window.show_view(game_view)

    def hit_medicine(self):
        if self.pet.sick:
            self.pet.care_score += 1

        self.pet.sick = False

    def hit_flush(self):
        self.pet.waste = False

    def hit_health_stats(self):
        if self.game_start:
            stats_view = StatsView(self.pet)
            stats_view.setup()
            self.window.show_view(stats_view)

    def hit_discipline(self):
        if self.pet.needs_attention is True and self.pet.sick is False and self.pet.waste is False and self.pet.hunger_meter > 2 and self.pet.mood_meter > 2:
            self.pet.discipline_meter += 1
            self.pet.needs_attention = False
        else:
            self.pet.care_score -= 1
            self.pet.mood_meter -= 1

    def hit_attention(self):
        self.pet.needs_attention = False


""" VIEWS FOR ACTIONS """
class EatView(SuperView):
    """ SETUP """
    def __init__(self, pet_object):
        super().__init__()
        self.eat_view_sprites = None
        self.pet = pet_object
        self.pet_list = None
        self.light_off = False


    def setup(self):
        super().setup()
        # pet
        self.pet_list = arcade.SpriteList()
        self.pet_list.append(self.pet)

    def on_draw(self):
        if self.pet.hunger_meter <= 4:
            super().on_draw()
            self.pet_list.draw()
            self.eat_view_sprites = arcade.SpriteList(is_static=True)

            # food
            food = arcade.Sprite(FOOD_IMG, FOOD_SCALE)
            food.center_x = 350
            food.center_y = 250
            self.eat_view_sprites.append(food)
            self.eat_view_sprites.draw()

        if self.pet.needs_attention:
            arcade.draw_rectangle_outline(505, 160, 75, 50, arcade.color.RED)

    def update(self, delta_time):
        self.pet_list.update_animation()

        # time
        self.pet.total_time += delta_time

    """ Main Game Loop Logic"""
    def hit_reset(self):
        main_view = MainView()
        main_view.setup()
        self.window.show_view(main_view)

    def hit_home(self):
        main_view = MainView(game_start=True, pet_object=self.pet)
        main_view.setup()
        self.window.show_view(main_view)

    def hit_eat(self):
        self.pet.is_eating = True

        if self.pet.hunger_meter <= 4:
            self.pet.care_score += 1
            self.pet.hunger_meter += 1

        if self.pet.hunger_meter <= 4:
            eat_view = EatView(self.pet)
            eat_view.setup()
            self.window.show_view(eat_view)

        elif self.pet.hunger_meter > 4:
            full_view = FullView(self.pet)
            full_view.setup()
            self.window.show_view(full_view)

    def hit_light(self):
        if self.light_off is False:
            self.light_off = True
            self.pet.care_score += 1
            dark_view = DarkView(self.pet)
            dark_view.setup()
            self.window.show_view(dark_view)

    def hit_game(self):

        # making sure the mood meter cannot exceed 4 to increase challenge
        if self.pet.mood_meter < 4:
            self.pet.mood_meter += 1
            self.pet.care_score += 1

        game_view = GameView(self.pet)
        game_view.setup()
        self.window.show_view(game_view)

    def hit_medicine(self):
        if self.pet.sick:
            self.pet.care_score += 1

        self.pet.sick = False

    def hit_flush(self):
        self.pet.waste = False

    def hit_health_stats(self):
        stats_view = StatsView(self.pet)
        stats_view.setup()
        self.window.show_view(stats_view)

    def hit_discipline(self):
        if self.pet.needs_attention is True and self.pet.sick is False and self.pet.waste is False and self.pet.hunger_meter > 2 and self.pet.mood_meter > 2:
            self.pet.discipline_meter += 1
            self.pet.needs_attention = False
        else:
            self.pet.mood_meter -= 1
            self.pet.care_score -= 1

    def hit_attention(self):
        self.pet.needs_attention = False


# full view
class FullView(SuperView):
    def __init__(self, pet_object):
        super().__init__()
        self.full_view_sprites = None
        self.pet = pet_object
        self.pet_list = None
        self.light_off = False

    def setup(self):
        super().setup()
        self.pet_list = arcade.SpriteList()
        self.pet_list.append(self.pet)

    def on_draw(self):
        if self.pet.hunger_meter > 4:
            super().on_draw()
            self.pet_list.draw()

            self.full_view_sprites = arcade.SpriteList(is_static=True)

            # full 'X' image
            x_full = arcade.Sprite(FULL_EX, FULL_SCALE)
            x_full.center_x = 300
            x_full.center_y = 380

            self.full_view_sprites.append(x_full)
            self.full_view_sprites.draw()

        if self.pet.needs_attention:
            arcade.draw_rectangle_outline(505, 160, 75, 50, arcade.color.RED)

    def update(self, delta_time):
        self.pet_list.update_animation()

        # time
        self.pet.total_time += delta_time

    """ Main Game Loop Logic"""
    def hit_reset(self):
        main_view = MainView()
        main_view.setup()
        self.window.show_view(main_view)

    def hit_home(self):
        self.pet.hunger_meter = 4
        main_view = MainView(game_start=True, pet_object=self.pet)
        main_view.setup()
        self.window.show_view(main_view)

    def hit_eat(self):
        pass

    def hit_light(self):
        self.pet.hunger_meter = 4
        if self.light_off is False:
            self.light_off = True
            self.pet.care_score += 1
            dark_view = DarkView(self.pet)
            dark_view.setup()
            self.window.show_view(dark_view)

    def hit_game(self):

        self.pet.hunger_meter = 4
        # making sure the mood meter cannot exceed 4 to increase challenge
        if self.pet.mood_meter < 4:
            self.pet.mood_meter += 1
            self.pet.care_score += 1

        game_view = GameView(self.pet)
        game_view.setup()
        self.window.show_view(game_view)

    def hit_medicine(self):
        if self.pet.sick:
            self.pet.care_score += 1

        self.pet.sick = False

    def hit_flush(self):
        self.pet.waste = False

    def hit_health_stats(self):
        self.pet.hunger_meter = 4
        stats_view = StatsView(self.pet)
        stats_view.setup()
        self.window.show_view(stats_view)

    def hit_discipline(self):
        if self.pet.needs_attention is True and self.pet.sick is False and self.pet.waste is False and self.pet.hunger_meter > 2 and self.pet.mood_meter > 2:
            self.pet.discipline_meter += 1
            self.pet.needs_attention = False
        else:
            self.pet.mood_meter -= 1
            self.pet.care_score -= 1

    def hit_attention(self):
        self.pet.needs_attention = False



# dark - lights off
class DarkView(SuperView):
    def __init__(self, pet_object):
        super().__init__()
        self.light_list = None
        self.pet = pet_object
        self.zsleep = None
        self.sleep_dark_panel_list = None


    def setup(self):
        super().setup()
        self.light_list = arcade.SpriteList(is_static=True)
        self.zsleep = arcade.Sprite(SLEEPING, SLEEPING_SCALE)
        self.zsleep.center_x = 270
        self.zsleep.center_y = 330
        self.light_list.append(self.zsleep)

        ## blacked out game screen
        self.sleep_dark_panel_list = arcade.ShapeElementList()
        dark_panel = arcade.create_rectangle_filled(center_x=300, center_y=340, width=550, height=300,
                                                      color=arcade.color.BLACK)
        self.sleep_dark_panel_list.append(dark_panel)

    def on_update(self, delta_time):
        # time
        self.pet.total_time += delta_time

    def on_draw(self):
        super().on_draw()

        self.sleep_dark_panel_list.draw()
        self.light_list.draw()

    def hit_light(self):
        main_view = MainView(game_start=True, pet_object=self.pet)
        main_view.setup()
        self.window.show_view(main_view)


class GameView(SuperView):
    def __init__(self, pet_object):
        super().__init__()
        self.game_view_sprites = None
        self.pet = pet_object
        self.pet_list = None
        self.light_off = False

    def setup(self):
        super().setup()
        self.pet_list = arcade.SpriteList()
        self.pet_list.append(self.pet)

    def on_draw(self):
        super().on_draw()
        self.pet_list.draw()
        self.game_view_sprites = arcade.SpriteList(is_static=True)

        # game controller
        game_controller = arcade.Sprite(GAME_IMG, GAME_SCALE)
        game_controller.center_x = 350
        game_controller.center_y = 300

        # heart
        heart = arcade.Sprite(HEART_IMG, HEART_SCALE)
        heart.center_x = 300
        heart.center_y = 380

        # append to game_view sprite list
        self.game_view_sprites.append(game_controller)
        self.game_view_sprites.append(heart)
        self.game_view_sprites.draw()

        if self.pet.needs_attention:
            arcade.draw_rectangle_outline(505, 160, 75, 50, arcade.color.RED)

    def update(self, delta_time):
        self.pet_list.update_animation()

        # time
        self.pet.total_time += delta_time

    """ Main Game Loop Logic"""
    def hit_reset(self):
        main_view = MainView()
        main_view.setup()
        self.window.show_view(main_view)

    def hit_home(self):
        main_view = MainView(game_start=True, pet_object=self.pet)
        main_view.setup()
        self.window.show_view(main_view)

    def hit_eat(self):
        self.pet.is_eating = True
        if self.pet.hunger_meter <= 4:
            self.pet.care_score += 1
            self.pet.hunger_meter += 1

        if self.pet.hunger_meter <= 4:
            eat_view = EatView(self.pet)
            eat_view.setup()
            self.window.show_view(eat_view)

        elif self.pet.hunger_meter > 4:
            full_view = FullView(self.pet)
            full_view.setup()
            self.window.show_view(full_view)

    def hit_light(self):
        if self.light_off is False:
            self.light_off = True
            self.pet.care_score += 1
            dark_view = DarkView(self.pet)
            dark_view.setup()
            self.window.show_view(dark_view)

    def hit_game(self):

        # making sure the mood meter cannot exceed 4 to increase challenge
        if self.pet.mood_meter < 4:
            self.pet.mood_meter += 1
            self.pet.care_score += 1

        game_view = GameView(self.pet)
        game_view.setup()
        self.window.show_view(game_view)

    def hit_medicine(self):
        if self.pet.sick:
            self.pet.care_score += 1

        self.pet.sick = False

    def hit_flush(self):
        self.pet.waste = False

    def hit_health_stats(self):
        stats_view = StatsView(self.pet)
        stats_view.setup()
        self.window.show_view(stats_view)

    def hit_discipline(self):
        if self.pet.needs_attention is True and self.pet.sick is False and self.pet.waste is False and self.pet.hunger_meter > 2 and self.pet.mood_meter > 2:
            self.pet.discipline_meter += 1
            self.pet.needs_attention = False
        else:
            self.pet.mood_meter -= 1
            self.pet.care_score -= 1

    def hit_attention(self):
        self.pet.needs_attention = False



class StatsView(SuperView):
    def __init__(self, pet_object):
        super().__init__()
        self.stats_view_sprites = None
        self.pet = pet_object
        self.pet_list = None
        self.discipline_level = None
        self.light_off = False

    def setup(self):
        super().setup()
        self.pet_list = arcade.SpriteList()
        self.pet_list.append(self.pet)
        self.stats_view_sprites = arcade.SpriteList(is_static=True)

        stat_y_coordinate = 460

        # blank hearts
        heart_1_blank = arcade.Sprite(BLANK_HEART, BLANK_HEART_SCALE)
        heart_1_blank.center_x = 300
        heart_1_blank.center_y = stat_y_coordinate

        heart_2_blank = arcade.Sprite(BLANK_HEART, BLANK_HEART_SCALE)
        heart_2_blank.center_x = 350
        heart_2_blank.center_y = stat_y_coordinate

        heart_3_blank = arcade.Sprite(BLANK_HEART, BLANK_HEART_SCALE)
        heart_3_blank.center_x = 400
        heart_3_blank.center_y = stat_y_coordinate

        heart_4_blank = arcade.Sprite(BLANK_HEART, BLANK_HEART_SCALE)
        heart_4_blank.center_x = 450
        heart_4_blank.center_y = stat_y_coordinate


        # full hearts
        heart_1_full = arcade.Sprite(HEART_IMG, HEART_SCALE)
        heart_1_full.center_x = 300
        heart_1_full.center_y = stat_y_coordinate

        heart_2_full = arcade.Sprite(HEART_IMG, HEART_SCALE)
        heart_2_full.center_x = 350
        heart_2_full.center_y = stat_y_coordinate

        heart_3_full = arcade.Sprite(HEART_IMG, HEART_SCALE)
        heart_3_full.center_x = 400
        heart_3_full.center_y = stat_y_coordinate

        heart_4_full = arcade.Sprite(HEART_IMG, HEART_SCALE)
        heart_4_full.center_x = 450
        heart_4_full.center_y = stat_y_coordinate

        # mood
        mood_x = 300
        mood_y = 410

        unhappy = arcade.Sprite(MOOD_UNHAPPY, MOOD_SCALE)
        unhappy.center_x = mood_x
        unhappy.center_y = mood_y

        ok = arcade.Sprite(MOOD_OK, MOOD_SCALE)
        ok.center_x = mood_x
        ok.center_y = mood_y

        neutral = arcade.Sprite(MOOD_NEUTRAL, MOOD_SCALE)
        neutral.center_x = mood_x
        neutral.center_y = mood_y

        happy = arcade.Sprite(MOOD_HAPPY, MOOD_SCALE)
        happy.center_x = mood_x
        happy.center_y = mood_y

        # text
        mood_text = arcade.Sprite(MOOD_TEXT, STAT_TEXT_SCALING)
        mood_text.center_x = 225
        mood_text.center_y = 410

        hunger_text = arcade.Sprite(HUNGER_TEXT, STAT_TEXT_SCALING)
        hunger_text.center_x = 225
        hunger_text.center_y = 460

        # always show stats text, append here
        self.stats_view_sprites.append(mood_text)
        self.stats_view_sprites.append(hunger_text)


        # logic for food
        if self.pet.hunger_meter == 0:
            self.stats_view_sprites.append(heart_1_blank)
            self.stats_view_sprites.append(heart_2_blank)
            self.stats_view_sprites.append(heart_3_blank)
            self.stats_view_sprites.append(heart_4_blank)

        elif self.pet.hunger_meter == 1:
            self.stats_view_sprites.append(heart_1_full)
            self.stats_view_sprites.append(heart_2_blank)
            self.stats_view_sprites.append(heart_3_blank)
            self.stats_view_sprites.append(heart_4_blank)

        elif self.pet.hunger_meter == 2:
            self.stats_view_sprites.append(heart_1_full)
            self.stats_view_sprites.append(heart_2_full)
            self.stats_view_sprites.append(heart_3_blank)
            self.stats_view_sprites.append(heart_4_blank)

        elif self.pet.hunger_meter == 3:
            self.stats_view_sprites.append(heart_1_full)
            self.stats_view_sprites.append(heart_2_full)
            self.stats_view_sprites.append(heart_3_full)
            self.stats_view_sprites.append(heart_4_blank)

        elif self.pet.hunger_meter >= 4:
            self.stats_view_sprites.append(heart_1_full)
            self.stats_view_sprites.append(heart_2_full)
            self.stats_view_sprites.append(heart_3_full)
            self.stats_view_sprites.append(heart_4_full)

        # logic for mood
        if self.pet.mood_meter == 0:
            self.stats_view_sprites.append(unhappy)

        elif self.pet.mood_meter == 1:
            self.stats_view_sprites.append(ok)

        elif self.pet.mood_meter == 2:
            self.stats_view_sprites.append(neutral)

        elif self.pet.mood_meter >= 3:
            self.stats_view_sprites.append(happy)

        # discipline logic
        if self.pet.discipline_meter is 0:
            self.discipline_level = "Wild"
        elif self.pet.discipline_meter <= 3:
            self.discipline_level = "Good"
        else:
            self.discipline_level = "Great"

    def on_draw(self):
        # draw the sprites appended based on the logic in setup
        super().on_draw()

        # draw hunger/mood stats
        self.stats_view_sprites.draw()
        self.pet_list.draw()

        if self.pet.needs_attention:
            arcade.draw_rectangle_outline(505, 160, 75, 50, arcade.color.RED)

    def update(self, delta_time):
        self.pet_list.update_animation()

        # time
        self.pet.total_time += delta_time

    """ Main Game Loop Logic"""
    def hit_reset(self):
        main_view = MainView()
        main_view.setup()
        self.window.show_view(main_view)

    def hit_home(self):
        main_view = MainView(game_start=True, pet_object=self.pet)
        main_view.setup()
        self.window.show_view(main_view)

    def hit_eat(self):
        self.pet.is_eating = True

        if self.pet.hunger_meter <= 4:
            self.pet.care_score += 1
            self.pet.hunger_meter += 1

        if self.pet.hunger_meter <= 4:
            eat_view = EatView(self.pet)
            eat_view.setup()
            self.window.show_view(eat_view)

        elif self.pet.hunger_meter > 4:
            full_view = FullView(self.pet)
            full_view.setup()
            self.window.show_view(full_view)

    def hit_light(self):
        if self.light_off is False:
            self.light_off = True
            self.pet.care_score += 1
            dark_view = DarkView(self.pet)
            dark_view.setup()
            self.window.show_view(dark_view)

    def hit_game(self):

        # making sure the mood meter cannot exceed 4 to increase challenge
        if self.pet.mood_meter < 4:
            self.pet.mood_meter += 1
            self.pet.care_score += 1

        game_view = GameView(self.pet)
        game_view.setup()
        self.window.show_view(game_view)

    def hit_medicine(self):
        if self.pet.sick:
            self.pet.care_score += 1

        self.pet.sick = False

    def hit_flush(self):
        self.pet.waste = False

    def hit_health_stats(self):
        stats_view = StatsView(self.pet)
        stats_view.setup()
        self.window.show_view(stats_view)

    def hit_discipline(self):
        if self.pet.needs_attention is True and self.pet.sick is False and self.pet.waste is False and self.pet.hunger_meter > 2 and self.pet.mood_meter > 2:
            self.pet.discipline_meter += 1
            self.pet.needs_attention = False
        else:
            self.pet.mood_meter -= 1
            self.pet.care_score -= 1

    def hit_attention(self):
        self.pet.needs_attention = False


""" Game Over View - TODO: COMPLETE """
class GameOverView(SuperView):
    """ SETUP """
    def __init__(self, pet_object):
        super().__init__()
        self.planet_list = None
        self.game_text_list = None
        self.gameover_dark_panel_list = None
        self.pet = pet_object
        self.final_score = 0

    def setup(self):
        super().setup()

        # planet
        self.planet_list = arcade.SpriteList(is_static=True)
        planet = arcade.Sprite(PLANET, PLANET_SCALE)
        planet.center_x = 100
        planet.center_y = 400
        self.planet_list.append(planet)

        # game over sign
        self.game_text_list = arcade.SpriteList(is_static=True)
        game_over_sign = arcade.Sprite(GAME_OVER, GAME_OVER_SCALE)
        game_over_sign.center_x = 300
        game_over_sign.center_y = 350
        self.game_text_list.append(game_over_sign)

        # dark panel
        self.gameover_dark_panel_list = arcade.ShapeElementList()
        dark_panel = arcade.create_rectangle_filled(center_x=300, center_y=340, width=550, height=300,
                                                      color=arcade.color.BLACK)
        self.gameover_dark_panel_list.append(dark_panel)


        self.final_score += self.pet.discipline_meter
        self.final_score = self.pet.care_score * 100

    def on_show(self):
        super().on_show()

    def on_draw(self):
        super().on_draw()

        self.gameover_dark_panel_list.draw()
        self.game_text_list.draw()
        arcade.draw_text("Final Score: " + str(self.final_score), 350, 450, arcade.color.WHITE, 16)
        self.planet_list.draw()

    def hit_reset(self):
        main_view = MainView()
        main_view.setup()
        self.window.show_view(main_view)





