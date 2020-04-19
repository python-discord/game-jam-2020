import arcade

SCREEN_SIZE = (800, 600)
TRIANGULATION_FREQUENCY = 0.1

BASE_SPEED = 1e-1
PLANET_BASE_SPEED = 5 * BASE_SPEED
PUSH_BASE_SPEED = 2 * BASE_SPEED
PUSH_MAX_DISTANCE = 200  # The most a planet can be away from Yogh to be pushed
BASE_DAMAGE = 1e-4
PLANET_DAMAGE = {
    "ze": 20,
    "yogh": 5,
    "ezh": 7
}
MAX_ATTACK_DISTANCE = {
    "ze": 100,
    "yogh": 300,
    "ezh": 300
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


SCREEN_TITLE = "Zeyoghezh"
ALL_PLANETS = ("ze", "yogh", "ezh")
