"""Game constants."""

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
FONT = ASSETS + 'ubuntu_{type}.ttf'
BACKGROUND = (25, 0, 50)
ABOUT = (
    'Gem Matcher was created by Artemis#8799 for the\n'
    '2020 Python Discord Game Jam. As per the\n'
    'competition rules, the game is written in Python\n'
    'and utilises Paul Craven\'s game library, Arcade.\n'
    'All graphics were created by Artemis#8799 using\n'
    'pixilart.com, and the font "Ubuntu" is used.'
)

ACHIEVEMENTS = [
    [
        {
            'description': 'Complete one game.',
            'name': 'Novice'
        },
        {
            'description': 'Complete ten games.',
            'name': 'Experienced'
        },
        {
            'description': 'Play one hundred games.',
            'name': 'Addicted'
        }
    ],
    [
        {
            'description': 'Get a point.',
            'name': 'Can play'
        },
        {
            'description': 'Get ten points.',
            'name': 'Getting the hang of it'
        },
        {
            'description': 'Get one hundred points.',
            'name': 'This is easy'
        }
    ],
    [
        {
            'description': 'Get a point.',
            'name': 'Three gems'
        },
        {
            'description': 'Get ten points in one game.',
            'name': 'High score!'
        },
        {
            'description': 'Get one hundred points in one game.',
            'name': 'That took a while...'
        }
    ],
    [
        {
            'description': 'Play for a minute.',
            'name': 'What\'s this!?'
        },
        {
            'description': 'Play for an hour.',
            'name': 'This is fun...'
        },
        {
            'description': 'Play for ten hours.',
            'name': 'All my spare time'
        }
    ]
]
