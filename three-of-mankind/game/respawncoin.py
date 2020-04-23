import time

import arcade

from game.utils import AnimLoader


class RespawnCoin(arcade.Sprite):
    anims = AnimLoader('assets/respawncoin')

    def update(self):
        self.texture = self.anims.generated[int(time.time() * 5 % len(self.anims.generated))]
