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
FONT = ASSETS + 'ubuntu_{}.ttf'
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
ABOUT = (
    'Gem Matcher was created by Artemis#8799 for the\n'
    '2020 Python Discord Game Jam. As per the\n'
    'competition rules, the game is written in Python\n'
    'and utilises Paul Craven\'s game library, Arcade.\n'
    'All graphics were created by Artemis#8799 using\n'
    'pixilart.com, and the font "Ubuntu" is used.'
)
ACHIEVMENTS = [
    {
        'type': 0,
        'level': 0,
        'description': 'Complete one game.',
        'name': 'Novice'
    },
    {
        'type': 0,
        'level': 1,
        'description': 'Complete ten games.',
        'name': 'Experienced'
    },
    {
        'type': 0,
        'level': 2,
        'description': 'Play one hundred games.',
        'name': 'Addicted'
    },
    {
        'type': 1,
        'level': 0,
        'description': 'Get a point.',
        'name': 'Can play'
    },
    {
        'type': 1,
        'level': 1,
        'description': 'Get ten points.',
        'name': 'Getting the hang of it'
    },
    {
        'type': 1,
        'level': 2,
        'description': 'Get one hundred points.',
        'name': 'This is easy'
    },
    {
        'type': 2,
        'level': 0,
        'description': 'Get a point.',
        'name': 'Three gems'
    },
    {
        'type': 2,
        'level': 1,
        'description': 'Get ten points in one game.',
        'name': 'High score!'
    },
    {
        'type': 2,
        'level': 1,
        'description': 'Get one hundred points in one game.',
        'name': 'That took a while...'
    },
    {
        'type': 3,
        'level': 0,
        'description': 'Play for a minute.',
        'name': 'What\'s this!?'
    },
    {
        'type': 3,
        'level': 1,
        'description': 'Play for an hour.',
        'name': 'This is fun...'
    },
    {
        'type': 3,
        'level': 2,
        'description': 'Play for ten hours.',
        'name': 'All my spare time'
    }
]