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
    'Oontz': Oontz,
    'Heal': Heal,
    'TribulletPowerup': TribulletPowerup,
    'AttackPowerup': AttackPowerup,
    'SpeedPowerup': SpeedPowerup,
    'Mirror': Mirror,
    'PortableHandMirror': PortableHandMirror,
    'Wall': Wall,
    'Star': Star,
    'Boom': Boom
}
arcade.run()
