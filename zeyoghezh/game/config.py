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

STORY_LINES = (
    "This is the story of three planets: Ze, Yogh, and Ezh.",
    "Each are made of one of the three elements of alchemy.",
    "Each are made of one of the three classes of combat.",
    "Each wishes to be the strongest, to destroy all others.",
    "And they each could do it.",
    "Ze, the silver one, could destroy Ezh, the bronze one.",
    "Yogh, the golden one, could destroy Ze, the silver one.",
    "Ezh, the bronze one, could destroy Yogh, the golden one.",
    "Yet if one is destroyed...",
    "...the three elements would be incomplete.",
    "We would be unable to fabricate the third periodic element.",
    "Lithium.",
    "Lithium is a valuable material, and each planet knows it.",
    "Each planet works to detect how far the nearest source is.",
    "But they cannot find it. For they cannot work together.",
    "Over time, ages to them but only seconds to you...",
    "...they will determine how far each source is.",
    "You can use all three. You can triangulate the location.",
    "You can bring this lithium home if you wish.",
    "But if the planets thrive...",
    "...they will guide you towards more.",
    "They, too, need lithium to survive.",
    "How much you reserve for home or for them is up to you.",
    "You must balance three tasks: ",
    "Collect lithium.",
    "heal wounded planets.",
    "And abscond when all is lost.",
    "Do not wait too long to abscond.",
    "You will need all three planets alive to escape.",
    "You must be curious about these planets.",
    "We are Ze. We are a planet of warriors.",
    "Our mines hold a treasure of Mercury.",
    "Our constellation is Rock.",
    "Our world is Silver.",
    "We are strong against Ezh.",
    "Their arrows do little damage...",
    "...and we need only get near them to crush them.",
    "We are weak against Yogh.",
    "Their mages keep us back...",
    "...while casting spells from a distance.",
    "...",
    "We are also Yogh. We are a planet of mages.",
    "We cast spells using the soil of our planet, Sulfur.",
    "Our constellation is Paper.",
    "Our world is Golden.",
    "We are strong against Ze.",
    "Our mages can keep them back...",
    "...while we cast spells from a distance.",
    "We are weak against Ezh.",
    "Their arrows fly faster than our blasts...",
    "...and pushing them away only strengthens them.",
    "...",
    "We are also Ezh. We are a planet of archers.",
    "Our arrows are tipped with chunks of our homeland, Salt.",
    "Our constellation is Scissors.",
    "Our world is Bronze.",
    "We are strong against Yogh.",
    "Our arrows fly faster than their blasts...",
    "...and pushing us away only strengthens us.",
    "We are weak against Ze.",
    "Our arrows do little damage...",
    "...and they need only get near us to crush us.",
    "...",
    "You are not one of us.",
    "Who are you?",
    "We are of three, but you are of four.",
    "You were not born here.",
    "You do not belong here.",
    # TODO add more
)
