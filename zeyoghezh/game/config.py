import arcade

SCREEN_SIZE = (800, 600)
TRIANGULATION_START_LIKELIHOOD = 0.02
TRIANGULATION_END_LIKELIHOOD = 0.05

BASE_SPEED = 1e-1  # TODO change to 1e-1 when this is over
PLANET_BASE_SPEED = 5 * BASE_SPEED
PUSH_BASE_SPEED = 3 * BASE_SPEED
PUSH_MAX_DISTANCE = 80  # The most a planet can be away from Yogh to be pushed
BASE_DAMAGE = 1e-4  # TODO change to 1e-4 when this is over
PLANET_DAMAGE = {
    "ze": 25,
    "yogh": 5,
    "ezh": 7
}
MAX_ATTACK_DISTANCE = {
    "ze": 60,
    "yogh": 100,
    "ezh": 100
}
PLANET_COLORS = {
    "ze": arcade.color.SILVER,
    "yogh": arcade.color.GOLD,
    "ezh": arcade.color.BRONZE
}
PLANET_SPRITES = {
    "ze": ":resources:images/items/coinSilver.png",
    "yogh": ":resources:images/items/coinGold.png",
    "ezh": ":resources:images/items/coinBronze.png"
}
ATTACK_SOUND = {
    "ze": ":resources:sounds/gameover3.wav",
    "yogh": ":resources:sounds/hurt2.wav",
    "ezh": ":resources:sounds/explosion1.wav"
}
BACKGROUND_IMAGE = "./game/space.jpg"
PUSH_SOUND = ":resources:sounds/upgrade1.wav"
# Music made by missingfragment#1983
BACKGROUND_MUSIC = "./game/music.ogg"
ATTACK_PLAYS_SOUND_CHANCE = 0.9

BACKGROUND_MUSIC_VOLUME = 0.5
SOUND_VOLUME = 1  # TODO use


SCREEN_TITLE = "Zeyoghezh"
ALL_PLANETS = ("ze", "yogh", "ezh")
