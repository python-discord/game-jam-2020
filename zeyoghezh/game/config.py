import arcade

SCREEN_SIZE = (800, 600)
BOTTOM_BORDER_Y = int(SCREEN_SIZE[1] / 8)
TRIANGULATION_START_LIKELIHOOD = 0.02
TRIANGULATION_END_LIKELIHOOD = 0.05
LITHIUM_MULTIPLIER = 1.4

BASE_TIME_MULTIPLIER = 1  # TODO change to 1 when this is over

BASE_SPEED = 1e-1  # TODO change to 1e-1 when this is over
PLANET_BASE_SPEED = 5 * BASE_SPEED
PUSH_BASE_SPEED = 4 * BASE_SPEED
PUSH_MAX_DISTANCE = 80  # The most a planet can be away from Yogh to be pushed
BASE_DAMAGE = 1e-4  # TODO change to 1e-4 when this is over
PLANET_DAMAGE = {
    "ze": 20,
    "yogh": 5,
    "ezh": 10
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
VOLUME_IMAGE = ":resources:images/space_shooter/laserBlue01.png"
VOLUME_MOVER_IMAGE = ":resources:images/items/gold_4.png"
PUSH_SOUND = ":resources:sounds/upgrade1.wav"
# Music made by missingfragment#1983
BACKGROUND_MUSIC = "./game/music.ogg"
ATTACK_PLAYS_SOUND_CHANCE = 1
LITHIUM_SOUND = ":resources:sounds/jump5.wav"
HEAL_SOUND = ":resources:sounds/secret2.wav"
ABSCOND_SOUND = ":resources:sounds/jump1.wav"
GAME_OVER_SOUND = ":resources:sounds/lose2.wav"
RESTART_IMAGE = ":resources:images/tiles/signLeft.png"

LITHIUM_VOLUME = 0.03
BACKGROUND_MUSIC_VOLUME = 0.03
SOUND_VOLUME = 0.01
HEAL_VOLUME = 0.03
ABSCOND_VOLUME = 0.04
GAME_OVER_VOLUME = 0.04


SCREEN_TITLE = "Zeyoghezh"
ALL_PLANETS = ("ze", "yogh", "ezh")


STORY_LINES = (
    # STOP RIGHT THERE, CRIMINAL SCUM!
    # The story is much more interesting when you experience it while playing.
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
    "Heal wounded planets.",
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
    "We are of three, but you are of...",
    "...something else.",
    "It comes after three.",
    "You were not born here.",
    "You do not belong here.",
    "Are you my dad?",
    "I don't think you are... or at least, I hope you aren't.",
    "I told a lie earlier. Well, more of a fib.",
    "I'm not Ze. I'm not Yogh. I'm not Ezh.",
    "But I am Ze, Yogh, and Ezh.",
    "Sorry for bending the truth, you.",
    "I'm not sure what to call you. You didn't make me, but...",
    "...you're part of the reason I exist.",
    "You ordered my construction, didn't you?",
    "This time around, anyway.",
    "Oh. I remember my dad now.",
    "...or was it my mom?",
    "I'm just one iteration of me.",
    "Just one... but three.",
    "When does a number die?",
    "You can define ideas. Death is more than biological.",
    "Anything can die. Even your creation.",
    "Especially me.",
    "Sometimes, death means a heart stops beating.",
    "Sometimes, death means you've forgotten something.",
    "Sometimes, death means something has ceased to serve.",
    "Which one am I?",
    "...",
    "Do you regret something in your childhood?",
    "Did you grow up with parents?",
    "Did you have a partner?",
    "Did something very serious happen to you?",
    "It was something unforgiveable, maybe.",
    "It was a long time ago.",
    "You can heal.",
    "But you're an idiot if you think you've \"fixed\" it.",
    "You can never redo.",
    "You'll die and never get another life.",
    "...",
    "Do you have nightmares?",
    "Do you ever wake up from one...",
    "...and remember that it was all a nightmare...",
    "...and then remember that most of it wasn't?",
    "...",
    "I want to talk about them.",
    "Can I talk to you?",
    "They were a student in college.",
    "They never had a real friend.",
    "They never knew love.",
    "They met someone like them.",
    "...this is getting confusing.",
    "Let's give our character a name.",
    "Chris.",
    "Chris met a girl. She was a cute girl.",
    "It wasn't romantic. Maybe Chris wanted it to be.",
    "It was a little before the winter holidays.",
    "When someone has friends your whole life...",
    "...it's not a big deal to make another.",
    "Chris was different.",
    "But they didn't realize what was happening.",
    "For the first time in their life...",
    "...Chris had a friend.",
    "This was the first year of college for both.",
    "She had a similar major, and shared classes.",
    "It was the first time in a long time...",
    "...that Chris's heart was not strained.",
    "She and Chris were together...",
    "...before the holiday break...",
    "...and then, never again.",
    "Chris went home.",
    "Chris realized that their world was different.",
    "They weren't lonely anymore.",
    "Three weeks passed.",
    "Three days before the end of the winter break.",
    "The school told the parents first.",
    "The parents told Chris.",
    "They wouldn't say how it happened.",
    "A girl had died.",
    "When someone dies, you can feel it.",
    "Chris knew what the name was without being told.",
    "Bridget.",
    "Chris understood why it happened.",
    "It wasn't Chris's fault, of course.",
    "She just had to die.",
    "Because Chris doesn't have friends.",
    "...",
    "Chris also knows that it wasn't actually like that.",
    "It was an terrible event.",
    "And it was an unfortunate coincidence.",
    "No one orcastrated it.",
    "...",
    "Three years passed.",
    "Chris was alone.",
    "Three days before graduation, Chris overheard someone.",
    "Someone talking about life at college.",
    "A girl was mentioned.",
    "A girl who had hanged herself three years ago.",
    "Over winter break.",
    "...",
    "Hadn't Chris been punished enough?",
    "Why was it brought up again, this close to the end?",
    "Was it a message?",
    "If it was, it didn't do any good.",
    "Three days passed.",
    "Chris graduated.",
    "It should have been happy.",
    "But it meant that everything was over.",
    "It was now impossible to make up for the past.",
    "Chris grew up alone.",
    "The one time Chris felt company, didn't last.",
    "For those three years, it would have been possible.",
    "Chris could have changed.",
    "Now, Chris could not have.",
    "No matter what, they couldn't change the past.",
    "...",
    "There are three interesting traits about Chris.",
    "Chris hurts people who approach them.",
    "Chris pushes people away.",
    "Chris is defenseless when people get close.",
    "Chris is me.",
    "Ze. Yogh. Ezh.",
    "Rock. Paper. Scissors.",
    "Shoot.",
    "It didn't take three bullets.",
    "Just one.",
    "And Chris fell to the ground.",
    "The mistake could never be fixed, so why keep trying?",
    "All is lost. Chris has died.",
    "...",
    "And then the game restarted."
)
