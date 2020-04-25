# imports and settings
import os
import random
from datetime import datetime, timedelta

import arcade

# Constants

# Pet scaling

# general
SPRITE_SCALING_PET = 4.8

""" SCALING BY AGE """
# toddler scaling
BABY_SCALE = 4.5
TODDLER_SCALE = 3.4
KID_SCALE = 4.5
YOUNG_ADULT_SCALE = 5.0
ADULT_SCALE = 5.0

""" --- Mouse Character --- """

## BABY

# normal
BABY_MOUSE_NORM = "./Animation/Tamogotchis/Mouse/Baby/MouseBabyTamogotchi_norm.png"
BABY_MOUSE_MOVE = "./Animation/Tamogotchis/Mouse/Baby/MouseBabyTamogotchi_move.png"

# full
BABY_MOUSE_FULL_L = "./Animation/Tamogotchis/Mouse/Baby/MouseBabyTamogotchi_full_left.png"
BABY_MOUSE_FULL_R = "./Animation/Tamogotchis/Mouse/Baby/MouseBabyTamogotchi_full_right.png"

# sick
BABY_MOUSE_SICK_MOVE = "./Animation/Tamogotchis/Mouse/Baby/MouseBabyTamogotchi_sickmove.png"
BABY_MOUSE_SICK_NORM = "./Animation/Tamogotchis/Mouse/Baby/MouseBabyTamogotchi_sicknorm.png"

## TODDLER

# normal
TODDLER_MOUSE_NORM = "./Animation/Tamogotchis/Mouse/Toddler/MouseToddlerTamogotchi32_norm.png"
TODDLER_MOUSE_MOVE = "./Animation/Tamogotchis/Mouse/Toddler/MouseToddlerTamogotchi32_move.png"

# full
TODDLER_MOUSE_FULL_L = "./Animation/Tamogotchis/Mouse/Toddler/MouseToddlerTamogotchi32_full_left.png"
TODDLER_MOUSE_FULL_R = "./Animation/Tamogotchis/Mouse/Toddler/MouseToddlerTamogotchi32_full_right.png"

# sick
TODDLER_MOUSE_SICK_NORM = "./Animation/Tamogotchis/Mouse/Toddler/MouseToddlerTamogotchi32_sicknorm.png"
TODDLER_MOUSE_SICK_MOVE = "./Animation/Tamogotchis/Mouse/Toddler/MouseToddlerTamogotchi32_sickmove.png"

## KID

# normal
KID_MOUSE_NORM = "./Animation/Tamogotchis/Mouse/Kid/KidTamogotchi_norm.png"
KID_MOUSE_MOVE = "./Animation/Tamogotchis/Mouse/Kid/KidTamogotchi_move.png"

# full
KID_MOUSE_FULL_L = "./Animation/Tamogotchis/Mouse/Kid/KidTamogotchi_full_left.png"
KID_MOUSE_FULL_R = "./Animation/Tamogotchis/Mouse/Kid/KidTamogotchi_full_right.png"

# sick
KID_MOUSE_SICK_NORM = "./Animation/Tamogotchis/Mouse/Kid/KidTamogotchi_sicknorm.png"
KID_MOUSE_SICK_MOVE = "./Animation/Tamogotchis/Mouse/Kid/KidTamogotchi_sickmove.png"

## YOUNG ADULT

# normal
YOUNG_ADULT_MOUSE_NORM = "./Animation/Tamogotchis/Mouse/YoungAdult/MouseYoungAdult_norm.png"
YOUNG_ADULT_MOUSE_MOVE = "./Animation/Tamogotchis/Mouse/YoungAdult/MouseYoungAdult_move.png"

# full
YOUNG_ADULT_FULL_MOUSE_L = "./Animation/Tamogotchis/Mouse/YoungAdult/MouseYoungAdult_full_left.png"
YOUNG_ADULT_FULL_MOUSE_R = "./Animation/Tamogotchis/Mouse/YoungAdult/MouseYoungAdult_full_right.png"

# sick
YOUNG_ADULT_MOUSE_SICK_NORM = "./Animation/Tamogotchis/Mouse/YoungAdult/MouseYoungAdult_sicknorm.png"
YOUNG_ADULT_MOUSE_SICK_MOVE = "./Animation/Tamogotchis/Mouse/YoungAdult/MouseYoungAdult_sickmove.png"

## ADULT

# normal
ADULT_MOUSE_NORM = "./Animation/Tamogotchis/Mouse/Adult/MouseAdult_norm.png"
ADULT_MOUSE_MOVE = "./Animation/Tamogotchis/Mouse/Adult/MouseAdult_move.png"

# full
ADULT_MOUSE_FULL_L = "./Animation/Tamogotchis/Mouse/Adult/MouseAdult_full_left.png"
ADULT_MOUSE_FULL_R = "./Animation/Tamogotchis/Mouse/Adult/MouseAdult_full_right.png"

# sick
ADULT_MOUSE_SICK_NORM = "./Animation/Tamogotchis/Mouse/Adult/MouseAdult_sicknorm.png"
ADULT_MOUSE_SICK_MOVE = "./Animation/Tamogotchis/Mouse/Adult/MouseAdult_sickmove.png"

""" --- Duck Character --- """

## BABY

# normal
BABY_DUCK_NORM = "./Animation/Tamogotchis/Duck/Baby/DuckBabyTamogotchi_norm.png"
BABY_DUCK_MOVE = "./Animation/Tamogotchis/Duck/Baby/DuckBabyTamogotchi_move.png"

# full
BABY_DUCK_FULL_L = "./Animation/Tamogotchis/Duck/Baby/DuckBabyTamogotchi_full_left.png"
BABY_DUCK_FULL_R = "./Animation/Tamogotchis/Duck/Baby/DuckBabyTamogotchi_full_right.png"

# sick
BABY_DUCK_SICK_NORM = "./Animation/Tamogotchis/Duck/Baby/DuckBabyTamogotchi_sicknorm.png"
BABY_DUCK_SICK_MOVE = "./Animation/Tamogotchis/Duck/Baby/DuckBabyTamogotchi_sickmove.png"

## TODDLER

# normal
TODDLER_DUCK_NORM = "./Animation/Tamogotchis/Duck/Toddler/DuckToddlerTamogotchi32_norm.png"
TODDLER_DUCK_MOVE = "./Animation/Tamogotchis/Duck/Toddler/DuckToddlerTamogotchi32_move.png"

# full
TODDLER_DUCK_FULL_L = "./Animation/Tamogotchis/Duck/Toddler/DuckToddlerTamogotchi32_full_left.png"
TODDLER_DUCK_FULL_R = "./Animation/Tamogotchis/Duck/Toddler/DuckToddlerTamogotchi32_full_right.png"

# sick
TODDLER_DUCK_SICK_NORM = "./Animation/Tamogotchis/Duck/Toddler/DuckToddlerTamogotchi32_sicknorm.png"
TODDLER_DUCK_SICK_MOVE = "./Animation/Tamogotchis/Duck/Toddler/DuckToddlerTamogotchi32_sickmove.png"

## KID

# normal
KID_DUCK_NORM = "./Animation/Tamogotchis/Duck/Kid/DuckKidTamogotchi_norm.png"
KID_DUCK_MOVE = "./Animation/Tamogotchis/Duck/Kid/DuckKidTamogotchi_move.png"

# full
KID_DUCK_FULL_L = "./Animation/Tamogotchis/Duck/Kid/DuckKidTamogotchi_full_left.png"
KID_DUCK_FULL_R = "./Animation/Tamogotchis/Duck/Kid/DuckKidTamogotchi_full_right.png"

# sick
KID_DUCK_SICK_NORM = "./Animation/Tamogotchis/Duck/Kid/DuckKidTamogotchi_sicknorm.png"
KID_DUCK_SICK_MOVE = "./Animation/Tamogotchis/Duck/Kid/DuckKidTamogotchi_sickmove.png"

## YOUNG ADULT

# normal
YOUNG_ADULT_DUCK_NORM = "./Animation/Tamogotchis/Duck/YoungAdult/DuckYoungAdultTamogotchi_norm.png"
YOUNG_ADULT_DUCK_MOVE = "./Animation/Tamogotchis/Duck/YoungAdult/DuckYoungAdultTamogotchi_move.png"

# full
YOUNG_ADULT_DUCK_FULL_L = "./Animation/Tamogotchis/Duck/YoungAdult/DuckYoungAdultTamogotchi_full_left.png"
YOUNG_ADULT_DUCK_FULL_R = "./Animation/Tamogotchis/Duck/YoungAdult/DuckYoungAdultTamogotchi_full_right.png"

# sick
YOUNG_ADULT_DUCK_SICK_NORM = "./Animation/Tamogotchis/Duck/YoungAdult/DuckYoungAdultTamogotchi_sicknorm.png"
YOUNG_ADULT_DUCK_SICK_MOVE = "./Animation/Tamogotchis/Duck/YoungAdult/DuckYoungAdultTamogotchi_sickmove.png"

## ADULT

# normal
ADULT_DUCK_NORM = "./Animation/Tamogotchis/Duck/Adult/DuckAdultTamogotchi_norm.png"
ADULT_DUCK_MOVE = "./Animation/Tamogotchis/Duck/Adult/DuckAdultTamogotchi_move.png"

# full
ADULT_DUCK_FULL_L = "./Animation/Tamogotchis/Duck/Adult/DuckAdultTamogotchi_full_left.png"
ADULT_DUCK_FULL_R = "./Animation/Tamogotchis/Duck/Adult/DuckAdultTamogotchi_full_right.png"

# sick
ADULT_DUCK_SICK_NORM = "./Animation/Tamogotchis/Duck/Adult/DuckAdultTamogotchi_sicknorm.png"
ADULT_DUCK_SICK_MOVE = "./Animation/Tamogotchis/Duck/Adult/DuckAdultTamogotchi_sickmove.png"

""" --- Sea Character --- """

## BABY

# normal
BABY_SEA_NORM = "./Animation/Tamogotchis/SeaCreature/Baby/SeaBabyTamogotchi_norm.png"
BABY_SEA_MOVE = "./Animation/Tamogotchis/SeaCreature/Baby/SeaBabyTamogotchi_move.png"

# full
BABY_SEA_FULL_L = "./Animation/Tamogotchis/SeaCreature/Baby/SeaBabyTamogotchi_full_left.png"
BABY_SEA_FULL_R = "./Animation/Tamogotchis/SeaCreature/Baby/SeaBabyTamogotchi_full_right.png"

# sick
BABY_SEA_SICK_NORM = "./Animation/Tamogotchis/SeaCreature/Baby/SeaBabyTamogotchi_sicknorm.png"
BABY_SEA_SICK_MOVE = "./Animation/Tamogotchis/SeaCreature/Baby/SeaBabyTamogotchi_sickmove.png"

## TODDLER

# normal
TODDLER_SEA_NORM = "./Animation/Tamogotchis/SeaCreature/Toddler/SeaToddlerTamogotchi32_norm.png"
TODDLER_SEA_MOVE = "./Animation/Tamogotchis/SeaCreature/Toddler/SeaToddlerTamogotchi32_move.png"

# full
TODDLER_SEA_FULL_L = "./Animation/Tamogotchis/SeaCreature/Toddler/SeaToddlerTamogotchi32_full_left.png"
TODDLER_SEA_FULL_R = "./Animation/Tamogotchis/SeaCreature/Toddler/SeaToddlerTamogotchi32_full_right.png"

# sick
TODDLER_SEA_SICK_NORM = "./Animation/Tamogotchis/SeaCreature/Toddler/SeaToddlerTamogotchi32_sicknorm.png"
TODDLER_SEA_SICK_MOVE = "./Animation/Tamogotchis/SeaCreature/Toddler/SeaToddlerTamogotchi32_sickmove.png"

## YOUNG ADULT

# normal
YOUNG_ADULT_SEA_NORM = "./Animation/Tamogotchis/SeaCreature/YoungAdult/SeaCreatureYoungAdult_norm.png"
YOUNG_ADULT_SEA_MOVE = "./Animation/Tamogotchis/SeaCreature/YoungAdult/SeaCreatureYoungAdult_move.png"

# full
YOUNG_ADULT_SEA_FULL_L = "./Animation/Tamogotchis/SeaCreature/YoungAdult/SeaCreatureYoungAdult_full_left.png"
YOUNG_ADULT_SEA_FULL_R = "./Animation/Tamogotchis/SeaCreature/YoungAdult/SeaCreatureYoungAdult_full_right.png"

# sick
YOUNG_ADULT_SEA_SICK_NORM = "./Animation/Tamogotchis/SeaCreature/YoungAdult/SeaCreatureYoungAdult_sicknorm.png"
YOUNG_ADULT_SEA_SICK_MOVE = "./Animation/Tamogotchis/SeaCreature/YoungAdult/SeaCreatureYoungAdult_sickmove.png"

## ADULT

# normal
ADULT_SEA_NORM = "./Animation/Tamogotchis/SeaCreature/Adult/SeaCreatureAdult_norm.png"
ADULT_SEA_MOVE = "./Animation/Tamogotchis/SeaCreature/Adult/SeaCreatureAdult_move.png"

# full
ADULT_SEA_FULL_L = "./Animation/Tamogotchis/SeaCreature/Adult/SeaCreatureAdult_full_left.png"
ADULT_SEA_FULL_R = "./Animation/Tamogotchis/SeaCreature/Adult/SeaCreatureAdult_full_right.png"

# sick
ADULT_SEA_SICK_NORM = "./Animation/Tamogotchis/SeaCreature/Adult/SeaCreatureAdult_sicknorm.png"
ADULT_SEA_SICK_MOVE = "./Animation/Tamogotchis/SeaCreature/Adult/SeaCreatureAdult_sickmove.png"

""" Alien Character - Only Displayed IF game won """
ALIEN_NORM = "./Animation/Tamogotchis/Alien/Alien_norm.png"
ALIEN_MOVE = "./Animation/Tamogotchis/Alien/Alien_move.png"


class PetCharacter(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__()

        """ Age logic """
        self.age = 0

        """ Pet time alive logic - feeds age """
        self.total_time = 0.0

        """ Species logic """
        # key translates whether the pet is going to be a mouse, duck, or sea creature
        self.pet_species_key = random.randrange(0, 3)

        """ Health/Sick Logic """
        self.sick = False

        """ Hunger Logic """
        self.hunger_meter = 0
        self.full = False

        """ Mood Logic """
        self.mood_meter = 0

        """ Disclipline/Attention """
        self.discipline_meter = 0
        self.needs_attention = False

        """ Waste Logic"""
        self.waste = False
        self.cur_texture = 0

        """ Score """
        self.care_score = 0

        """ Scale - adjusted based on pet age in animation updates """
        self.scale = BABY_SCALE

        """ ===UPDATED CHARACTER TEXTURES=== """

        """ --- MOUSE -- """

        ## mouse baby
        # normal
        self.mouse_baby_normal_textures = []
        self.mouse_baby_normal_textures.append(arcade.load_texture(file_name=BABY_MOUSE_NORM))
        self.mouse_baby_normal_textures.append(arcade.load_texture(file_name=BABY_MOUSE_MOVE))

        # full
        self.mouse_baby_full_textures = []
        self.mouse_baby_full_textures.append(arcade.load_texture(file_name=BABY_MOUSE_FULL_R))
        self.mouse_baby_full_textures.append(arcade.load_texture(file_name=BABY_MOUSE_FULL_L))

        # sick
        self.mouse_baby_sick_textures = []
        self.mouse_baby_sick_textures.append(arcade.load_texture(file_name=BABY_MOUSE_SICK_NORM))
        self.mouse_baby_sick_textures.append(arcade.load_texture(file_name=BABY_MOUSE_SICK_MOVE))

        ## mouse toddler
        # normal
        self.mouse_toddler_normal_textures = []
        self.mouse_toddler_normal_textures.append(arcade.load_texture(file_name=TODDLER_MOUSE_NORM))
        self.mouse_toddler_normal_textures.append(arcade.load_texture(file_name=TODDLER_MOUSE_MOVE))

        # full
        self.mouse_toddler_full_textures = []
        self.mouse_toddler_full_textures.append(arcade.load_texture(file_name=TODDLER_MOUSE_FULL_L))
        self.mouse_toddler_full_textures.append(arcade.load_texture(file_name=TODDLER_MOUSE_FULL_R))

        # sick
        self.mouse_toddler_sick_textures = []
        self.mouse_toddler_sick_textures.append(arcade.load_texture(file_name=TODDLER_MOUSE_SICK_NORM))
        self.mouse_toddler_sick_textures.append(arcade.load_texture(file_name=TODDLER_MOUSE_SICK_MOVE))

        ## mouse kid
        self.mouse_kid_normal_textures = []
        self.mouse_kid_normal_textures.append(arcade.load_texture(file_name=KID_MOUSE_NORM))
        self.mouse_kid_normal_textures.append(arcade.load_texture(file_name=KID_MOUSE_MOVE))

        self.mouse_kid_full_textures = []
        self.mouse_kid_full_textures.append(arcade.load_texture(file_name=KID_MOUSE_FULL_L))
        self.mouse_kid_full_textures.append(arcade.load_texture(file_name=KID_MOUSE_FULL_R))

        self.mouse_kid_sick_textures = []
        self.mouse_kid_sick_textures.append(arcade.load_texture(file_name=KID_MOUSE_SICK_NORM))
        self.mouse_kid_sick_textures.append(arcade.load_texture(file_name=KID_MOUSE_SICK_MOVE))

        ## mouse young adult
        self.mouse_young_adult_normal_textures = []
        self.mouse_young_adult_normal_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_MOUSE_NORM))
        self.mouse_young_adult_normal_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_MOUSE_MOVE))

        self.mouse_young_adult_full_textures = []
        self.mouse_young_adult_full_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_FULL_MOUSE_L))
        self.mouse_young_adult_full_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_FULL_MOUSE_R))

        self.mouse_young_adult_sick_textures = []
        self.mouse_young_adult_sick_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_MOUSE_SICK_NORM))
        self.mouse_young_adult_sick_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_MOUSE_SICK_MOVE))

        ## mouse adult
        self.mouse_adult_normal_textures = []
        self.mouse_adult_normal_textures.append(arcade.load_texture(file_name=ADULT_MOUSE_NORM))
        self.mouse_adult_normal_textures.append(arcade.load_texture(file_name=ADULT_MOUSE_MOVE))

        self.mouse_adult_full_textures = []
        self.mouse_adult_full_textures.append(arcade.load_texture(file_name=ADULT_MOUSE_FULL_L))
        self.mouse_adult_full_textures.append(arcade.load_texture(file_name=ADULT_MOUSE_FULL_R))

        self.mouse_adult_sick_textures = []
        self.mouse_adult_sick_textures.append(arcade.load_texture(file_name=ADULT_MOUSE_SICK_NORM))
        self.mouse_adult_sick_textures.append(arcade.load_texture(file_name=ADULT_MOUSE_SICK_MOVE))

        """ --- DUCK -- """

        ## duck baby
        # normal
        self.duck_baby_normal_textures = []
        self.duck_baby_normal_textures.append(arcade.load_texture(file_name=BABY_DUCK_NORM))
        self.duck_baby_normal_textures.append(arcade.load_texture(file_name=BABY_DUCK_MOVE))

        # full
        self.duck_baby_full_textures = []
        self.duck_baby_full_textures.append(arcade.load_texture(file_name=BABY_DUCK_FULL_R))
        self.duck_baby_full_textures.append(arcade.load_texture(file_name=BABY_DUCK_FULL_L))

        # sick
        self.duck_baby_sick_textures = []
        self.duck_baby_sick_textures.append(arcade.load_texture(file_name=BABY_DUCK_SICK_NORM))
        self.duck_baby_sick_textures.append(arcade.load_texture(file_name=BABY_DUCK_SICK_MOVE))

        ## duck toddler
        # normal
        self.duck_toddler_normal_textures = []
        self.duck_toddler_normal_textures.append(arcade.load_texture(file_name=TODDLER_DUCK_NORM))
        self.duck_toddler_normal_textures.append(arcade.load_texture(file_name=TODDLER_DUCK_MOVE))

        # full
        self.duck_toddler_full_textures = []
        self.duck_toddler_full_textures.append(arcade.load_texture(file_name=TODDLER_DUCK_FULL_L))
        self.duck_toddler_full_textures.append(arcade.load_texture(file_name=TODDLER_DUCK_FULL_R))

        # sick
        self.duck_toddler_sick_textures = []
        self.duck_toddler_sick_textures.append(arcade.load_texture(file_name=TODDLER_DUCK_SICK_NORM))
        self.duck_toddler_sick_textures.append(arcade.load_texture(file_name=TODDLER_DUCK_SICK_MOVE))

        ## duck kid
        self.duck_kid_normal_textures = []
        self.duck_kid_normal_textures.append(arcade.load_texture(file_name=KID_DUCK_NORM))
        self.duck_kid_normal_textures.append(arcade.load_texture(file_name=KID_DUCK_MOVE))

        self.duck_kid_full_textures = []
        self.duck_kid_full_textures.append(arcade.load_texture(file_name=KID_DUCK_FULL_L))
        self.duck_kid_full_textures.append(arcade.load_texture(file_name=KID_DUCK_FULL_R))

        self.duck_kid_sick_textures = []
        self.duck_kid_sick_textures.append(arcade.load_texture(file_name=KID_DUCK_SICK_NORM))
        self.duck_kid_sick_textures.append(arcade.load_texture(file_name=KID_DUCK_SICK_MOVE))

        ## duck young adult
        # normal
        self.duck_young_adult_normal_textures = []
        self.duck_young_adult_normal_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_DUCK_NORM))
        self.duck_young_adult_normal_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_DUCK_MOVE))

        # full
        self.duck_young_adult_full_textures = []
        self.duck_young_adult_full_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_DUCK_FULL_L))
        self.duck_young_adult_full_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_DUCK_FULL_R))

        # sick
        self.duck_young_adult_sick_textures = []
        self.duck_young_adult_sick_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_DUCK_SICK_NORM))
        self.duck_young_adult_sick_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_DUCK_SICK_MOVE))

        ## duck adult
        # normal
        self.duck_adult_normal_textures = []
        self.duck_adult_normal_textures.append(arcade.load_texture(file_name=ADULT_DUCK_NORM))
        self.duck_adult_normal_textures.append(arcade.load_texture(file_name=ADULT_DUCK_MOVE))

        # full
        self.duck_adult_full_textures = []
        self.duck_adult_full_textures.append(arcade.load_texture(file_name=ADULT_DUCK_FULL_L))
        self.duck_adult_full_textures.append(arcade.load_texture(file_name=ADULT_DUCK_FULL_R))

        # sick
        self.duck_adult_sick_textures = []
        self.duck_adult_sick_textures.append(arcade.load_texture(file_name=ADULT_DUCK_SICK_NORM))
        self.duck_adult_sick_textures.append(arcade.load_texture(file_name=ADULT_DUCK_SICK_MOVE))

        """ --- SEA CREATURE -- """

        ## sea baby
        # normal
        self.sea_baby_normal_textures = []
        self.sea_baby_normal_textures.append(arcade.load_texture(file_name=BABY_SEA_NORM))
        self.sea_baby_normal_textures.append(arcade.load_texture(file_name=BABY_SEA_MOVE))

        # full
        self.sea_baby_full_textures = []
        self.sea_baby_full_textures.append(arcade.load_texture(file_name=BABY_SEA_FULL_R))
        self.sea_baby_full_textures.append(arcade.load_texture(file_name=BABY_SEA_FULL_L))

        # sick
        self.sea_baby_sick_textures = []
        self.sea_baby_sick_textures.append(arcade.load_texture(file_name=BABY_SEA_SICK_NORM))
        self.sea_baby_sick_textures.append(arcade.load_texture(file_name=BABY_SEA_SICK_MOVE))

        ## sea toddler
        # normal
        self.sea_toddler_normal_textures = []
        self.sea_toddler_normal_textures.append(arcade.load_texture(file_name=TODDLER_SEA_NORM))
        self.sea_toddler_normal_textures.append(arcade.load_texture(file_name=TODDLER_SEA_MOVE))

        # full
        self.sea_toddler_full_textures = []
        self.sea_toddler_full_textures.append(arcade.load_texture(file_name=TODDLER_SEA_FULL_L))
        self.sea_toddler_full_textures.append(arcade.load_texture(file_name=TODDLER_SEA_FULL_R))

        # sick
        self.sea_toddler_sick_textures = []
        self.sea_toddler_sick_textures.append(arcade.load_texture(file_name=TODDLER_SEA_SICK_NORM))
        self.sea_toddler_sick_textures.append(arcade.load_texture(file_name=TODDLER_SEA_SICK_MOVE))

        ## NOTE - SEA DOES NOT HAVE KID

        ## sea young adult
        # normal
        self.sea_young_adult_normal_textures = []
        self.sea_young_adult_normal_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_SEA_NORM))
        self.sea_young_adult_normal_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_SEA_MOVE))

        # full
        self.sea_young_adult_full_textures = []
        self.sea_young_adult_full_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_SEA_FULL_L))
        self.sea_young_adult_full_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_SEA_FULL_R))

        # sick
        self.sea_young_adult_sick_textures = []
        self.sea_young_adult_sick_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_SEA_SICK_NORM))
        self.sea_young_adult_sick_textures.append(arcade.load_texture(file_name=YOUNG_ADULT_SEA_SICK_MOVE))

        ## sea adult
        # normal
        self.sea_adult_normal_textures = []
        self.sea_adult_normal_textures.append(arcade.load_texture(file_name=ADULT_SEA_NORM))
        self.sea_adult_normal_textures.append(arcade.load_texture(file_name=ADULT_SEA_MOVE))

        # full
        self.sea_adult_full_textures = []
        self.sea_adult_full_textures.append(arcade.load_texture(file_name=ADULT_SEA_FULL_L))
        self.sea_adult_full_textures.append(arcade.load_texture(file_name=ADULT_SEA_FULL_R))

        # sick
        self.sea_adult_sick_textures = []
        self.sea_adult_sick_textures.append(arcade.load_texture(file_name=ADULT_SEA_SICK_NORM))
        self.sea_adult_sick_textures.append(arcade.load_texture(file_name=ADULT_SEA_SICK_MOVE))

        """ --- ALIEN -- """
        self.alien_textures = []
        self.alien_textures.append(arcade.load_texture(file_name=ALIEN_NORM))
        self.alien_textures.append(arcade.load_texture(file_name=ALIEN_MOVE))

        """ Pet coordinates """
        self.center_x = 275
        self.center_y = 300

    def update_animation(self, delta_time: float = 1 / 60):
        # TODO: Add Scaling

        """ MOUSE """
        if self.pet_species_key is 0:

            # baby
            if self.age < 2:
                self.scale = BABY_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.mouse_baby_normal_textures[
                            random.randrange(len(self.mouse_baby_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.mouse_baby_sick_textures[
                            random.randrange(len(self.mouse_baby_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.mouse_baby_full_textures[random.randrange(len(self.mouse_baby_full_textures))]

            # toddler
            if self.age >= 2 and self.age < 5:
                self.scale = TODDLER_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.mouse_toddler_normal_textures[
                            random.randrange(len(self.mouse_toddler_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.mouse_toddler_sick_textures[
                            random.randrange(len(self.mouse_toddler_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.mouse_toddler_full_textures[
                        random.randrange(len(self.mouse_toddler_full_textures))]

            # kid
            if self.age >= 5 and self.age < 7:
                self.scale = KID_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.mouse_kid_normal_textures[
                            random.randrange(len(self.mouse_kid_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.mouse_kid_sick_textures[random.randrange(len(self.mouse_kid_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.mouse_kid_full_textures[random.randrange(len(self.mouse_kid_full_textures))]

            # young adult
            if self.age >= 7 and self.age < 9:
                self.scale = YOUNG_ADULT_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.mouse_young_adult_normal_textures[
                            random.randrange(len(self.mouse_young_adult_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.mouse_young_adult_sick_textures[
                            random.randrange(len(self.mouse_young_adult_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.mouse_young_adult_full_textures[
                        random.randrange(len(self.mouse_young_adult_full_textures))]

            # adult
            if self.age >= 9 and self.age < 12:
                self.scale = ADULT_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.mouse_adult_normal_textures[
                            random.randrange(len(self.mouse_adult_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.mouse_adult_sick_textures[
                            random.randrange(len(self.mouse_adult_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.mouse_adult_full_textures[random.randrange(len(self.mouse_adult_full_textures))]

        """ DUCK """
        if self.pet_species_key is 1:

            # baby
            if self.age < 2:
                self.scale = BABY_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.duck_baby_normal_textures[
                            random.randrange(len(self.duck_baby_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.duck_baby_sick_textures[random.randrange(len(self.duck_baby_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.duck_baby_full_textures[random.randrange(len(self.duck_baby_full_textures))]

            # toddler
            if self.age >= 2 and self.age < 5:
                self.scale = TODDLER_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.duck_toddler_normal_textures[
                            random.randrange(len(self.duck_toddler_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.duck_toddler_sick_textures[
                            random.randrange(len(self.duck_toddler_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.duck_toddler_full_textures[
                        random.randrange(len(self.duck_toddler_full_textures))]

            # kid
            if self.age >= 5 and self.age < 7:
                self.scale = KID_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.duck_kid_normal_textures[
                            random.randrange(len(self.duck_kid_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.duck_kid_sick_textures[random.randrange(len(self.duck_kid_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.duck_kid_full_textures[random.randrange(len(self.duck_kid_full_textures))]

            # young adult
            if self.age >= 7 and self.age < 9:
                self.scale = YOUNG_ADULT_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.duck_young_adult_normal_textures[
                            random.randrange(len(self.duck_young_adult_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.duck_young_adult_sick_textures[
                            random.randrange(len(self.duck_young_adult_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.duck_young_adult_full_textures[
                        random.randrange(len(self.duck_young_adult_full_textures))]

            # adult
            if self.age >= 9 and self.age < 12:
                self.scale = ADULT_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.duck_adult_normal_textures[
                            random.randrange(len(self.duck_adult_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.duck_adult_sick_textures[
                            random.randrange(len(self.duck_adult_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.duck_adult_full_textures[random.randrange(len(self.duck_adult_full_textures))]

        """ SEA CREATURE """
        if self.pet_species_key is 2:

            if self.age < 2:
                self.scale = BABY_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.sea_baby_normal_textures[
                            random.randrange(len(self.sea_baby_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.sea_baby_sick_textures[random.randrange(len(self.sea_baby_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.sea_baby_full_textures[random.randrange(len(self.sea_baby_full_textures))]

            # toddler
            if self.age >= 2 and self.age < 5:
                self.scale = TODDLER_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.sea_toddler_normal_textures[
                            random.randrange(len(self.sea_toddler_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.sea_toddler_sick_textures[
                            random.randrange(len(self.sea_toddler_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.sea_toddler_full_textures[random.randrange(len(self.sea_toddler_full_textures))]

            # Sea Creature does not have kid phase
            # young adult - PICK UP HERE CHANGING TEXTURES TO SEA CREATURE
            if self.age >= 5 and self.age < 9:
                self.scale = YOUNG_ADULT_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.sea_young_adult_normal_textures[
                            random.randrange(len(self.sea_young_adult_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.sea_young_adult_sick_textures[
                            random.randrange(len(self.sea_young_adult_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.sea_young_adult_full_textures[
                        random.randrange(len(self.sea_young_adult_full_textures))]

            if self.age >= 9 and self.age < 12:
                self.scale = ADULT_SCALE
                if self.hunger_meter <= 4:
                    if self.sick is False:
                        self.texture = self.sea_adult_normal_textures[
                            random.randrange(len(self.sea_adult_normal_textures))]
                    elif self.sick is True:
                        self.texture = self.sea_adult_sick_textures[random.randrange(len(self.sea_adult_sick_textures))]
                elif self.hunger_meter > 4:
                    self.texture = self.sea_adult_full_textures[random.randrange(len(self.sea_adult_full_textures))]

        if self.age >= 12:
            self.texture = self.alien_textures[random.randrange(len(self.alien_textures))]
