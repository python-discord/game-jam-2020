from game import *

import arcade

window.classes = {
    'Player': Player,
    'Bullet': Bullet,
    'TriBullet': TriBullet,
    'Waffle': Waffle,
    'Reggae': Reggae,
    'Sniper': Sniper,
    'Whiffle': Whiffle,
    'Oontz': Oontz
}
window.setup()
arcade.run()
