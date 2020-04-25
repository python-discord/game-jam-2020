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
GRAVITY = 5 * SCALING

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
MULTIPLAYER_HELP = (
    'In multiplayer mode, two or three players fight to\n'
    'get the most points. Each player controls a seperate\n'
    'blob, and must get gems before other players, or\n'
    'push their opponents into spikes. You have ninety\n'
    'seconds to get points, however if you die, your\n'
    'points reset. Be careful!'
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
    ],
]

AWARDS = [
    {
        'description': 'Get a point using no common gems.',
        'name': 'All in white'
    },
    {
        'description': 'Restart four times in a row.',
        'name': 'The perfect spawn'
    },
    {
        'description': 'Get a point while having two pink gems.',
        'name': 'I like pink'
    },
    {
        'description': 'Get a red, yellow and blue set in one game.',
        'name': 'Gotta catch em all'
    },
    {
        'description': 'Get a set without any white gems in.',
        'name': 'Wildcards are for the weak',
    },
    {
        'description': 'Score exactly 69.',
        'name': 'The perfect score doesn\'t ex-'
    },
]
