import random
import time

import arcade

from triple_vision.cards import CardManager
from triple_vision.constants import (
    SCALED_TILE,
    SCALING,
    WINDOW_SIZE,
)
from triple_vision.entities import (
    ChasingEnemy,
    Enemies,
    Player,
    LaserProjectile,
)


class TripleVision(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.paused = False

        self.tiles = None

        self.player = None
        self.enemy = None

        self.bullet_list = None

        self.card_manager = None

        self.physics_engine = None

    def setup(self) -> None:
        self.tiles = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        for y in range(0, WINDOW_SIZE[1], SCALED_TILE):
            for x in range(0, WINDOW_SIZE[0], SCALED_TILE):
                self.tiles.append(
                    arcade.Sprite(
                        filename=f'assets/dungeon/frames/floor_{random.randint(1, 8)}.png',
                        scale=SCALING,
                        center_x=x + SCALED_TILE / 2,
                        center_y=y + SCALED_TILE / 2
                    )
                )

        self.player = Player('m')
        self.enemy = ChasingEnemy(Enemies.big_demon,
                                  self.player,
                                  SCALED_TILE * 10,
                                  moving_speed=1,
                                  center_x=50,
                                  center_y=500)
        self.card_manager = CardManager(self)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.card_manager.check_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if not self.card_manager.check_mouse_press(x, y, button):
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.player.move_to(x, y, rotate=False)
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                if time.time() - self.player.last_shot < 0.75:  # TODO hardcoded
                    # TODO Play empty gun sound or something similar
                    return
                bullet = LaserProjectile(
                    center_x=self.player.center_x, center_y=self.player.center_y
                )
                bullet.move_to(x, y, rotate=True, set_target=False)
                self.bullet_list.append(bullet)
                self.player.last_shot = time.time()

    # def on_key_press(self, key, modifiers):
    #     """Called whenever a key is pressed. """
    #
    #     vec = [0, 0]
    #     if time.time() - self.last_key_data[1] < PRESSING_DELAY:
    #         last_key = self.last_key_data[0]
    #         if sorted((key, last_key)) == [arcade.key.LEFT, arcade.key.UP]:
    #             vec = [-1, 1]
    #         if sorted((key, last_key)) == [arcade.key.UP, arcade.key.RIGHT]:
    #             vec = [1, 1]
    #         if sorted((key, last_key)) == [arcade.key.LEFT, arcade.key.DOWN]:
    #             vec = [-1, -1]
    #         if sorted((key, last_key)) == [arcade.key.RIGHT, arcade.key.DOWN]:
    #             vec = [1, -1]
    #     elif key == arcade.key.UP:
    #         vec[1] = 1
    #     elif key == arcade.key.DOWN:
    #         vec[1] = -1
    #     elif key == arcade.key.LEFT:
    #         vec[0] = -1
    #     elif key == arcade.key.RIGHT:
    #         vec[0] = 1
    #
    #     print(f"Vec: {vec}")
    #
    #     self.last_key_data = [key, time.time()]
    #
    #     bullet = Bullet(
    #         BULLET_LIFETIME,
    #         BULLET_SPEED,
    #         ":resources:images/space_shooter/laserBlue01.png",
    #         center_x=self.player.center_x, center_y=self.player.center_y
    #     )
    #     bullet.move_to_angle(math.atan2(vec[1], vec[0]))
    #     self.bullet_list.append(bullet)

    def on_draw(self) -> None:
        self.tiles.draw()
        self.bullet_list.draw()
        self.player.draw()
        self.enemy.draw()
        self.card_manager.draw()

    def on_update(self, delta_time: float) -> None:
        if not self.paused:
            self.bullet_list.update()
            self.player.update(delta_time)
            self.enemy.update(delta_time)

            for projectile in self.bullet_list:
                if arcade.check_for_collision(projectile, self.enemy):
                    self.enemy.hit(projectile.dmg, projectile, projectile.throwback_force, tuple())
                    projectile.kill()

        self.card_manager.update()
