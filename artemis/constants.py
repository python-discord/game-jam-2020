BLOCKS_Y = 20
BLOCKS_X = 40
SCALING = 0.25
HEIGHT = int(BLOCKS_Y * SCALING * 128)
WIDTH = int(BLOCKS_X * SCALING * 128)
SIDE = WIDTH // 2
BLOCKS_TOP = 5
TOP = int(BLOCKS_TOP * SCALING * 128)

SPEED = 20 * SCALING
GRAVITY = 10 * SCALING

ASSETS = 'assets/'
BACKGROUND = (25, 0, 50)
INSTRUCTIONS = (
    'You will play a green slime, moving along the walls\n'
    'of a tunnel. Your aim is to collect gems. To\n'
    'collect a gem, simply collide with it. However: you\n'
    'only have five spaces in your inventory. If these \n'
    'five spaces fill up, the game is over! This is\n'
    'where the color of gems is important: there are\n'
    'red, yellow, blue and white and pink gems. If you\n'
    'have three red, yellow or blue gems in your\n'
    'inventory, they disappear and instead, you get a\n'
    'point. White gems act as wild cards. For example,\n'
    'if you had two red gems and a white gem, they would\n'
    'all disappear and be replaced with a point. Pink\n'
    'gems are impossible to get rid of: once they\'re in\n'
    'your inventory, they are impossible to get rid of -\n'
    'essentially, they reduce the size of your inventory.\n'
    'The aim is to collect as many points as possible.\n'
    'There is only one control, press any key to use it;\n'
    'this control will invert gravity - if you were\n'
    'being pulled down, you will now be pulled up, and\n'
    'vice versa. Make sure not to hit any spikes, and\n'
    'Good luck!'
)