from typing import Tuple

import arcade

from triple_vision import Settings as s
from triple_vision.entities import DamageIndicator


class GameManager:

    def __init__(self, view) -> None:
        self.view = view

        self.enemies = arcade.SpriteList()
        self.player_projectiles = arcade.SpriteList()
        self.enemy_projectiles = arcade.SpriteList()
        self.damage_indicators = arcade.SpriteList()

    def draw(self) -> None:
        self.enemies.draw()
        self.player_projectiles.draw()
        self.enemy_projectiles.draw()
        self.damage_indicators.draw()

    def create_enemy(self, enemy_class, *args, **kwargs) -> None:
        enemy = enemy_class(self, *args, **kwargs)
        self.enemies.append(enemy)

    def create_dmg_indicator(self, text: str, position: Tuple[float, float]) -> None:
        dmg_indicator = DamageIndicator(text, *position)
        self.damage_indicators.append(dmg_indicator)

    def on_update(self, delta_time) -> None:
        for enemy in self.enemies:
            for projectile in self.player_projectiles:
                if arcade.check_for_collision(projectile, enemy):
                    self.create_dmg_indicator(str(projectile.dmg), enemy.position)
                    enemy.hit(projectile)
                    projectile.kill()

        for projectile in self.enemy_projectiles:
            if arcade.check_for_collision(projectile, self.view.player):
                self.view.player.hit(projectile)
                projectile.kill()

        self.enemies.on_update(delta_time)
        self.player_projectiles.on_update(delta_time)
        self.enemy_projectiles.on_update(delta_time)
        self.damage_indicators.on_update(delta_time)


class CardManager:

    def __init__(self, view) -> None:
        self.view = view

        self.cards = arcade.SpriteList()
        self.colors = ('red', 'green', 'blue')

        card_scale = s.SCALING / 6

        self.MIN_CARD_HEIGHT = -132 * card_scale
        self.MAX_CARD_HEIGHT = 84 * card_scale
        self.MAX_CARD_HOVER_HEIGHT = 280 * card_scale

        for idx, color in enumerate(self.colors):
            self.cards.append(
                arcade.Sprite(
                    filename=f'assets/wizard/{color}_card.png',
                    scale=card_scale,
                    center_x=s.WINDOW_SIZE[0] / 2 + (idx - 1) * 400 * card_scale,
                    center_y=self.MIN_CARD_HEIGHT
                )
            )

        self.show_cards = False
        self.hover_card = None
        self.prev_hover_card = None

        self.prev_viewport = self.view.camera.viewport_left, self.view.camera.viewport_bottom

    def set_hover_card(self, card):
        if card != self.hover_card:
            self.prev_hover_card = self.hover_card
            self.hover_card = card

    def check_mouse_motion(self, x, y) -> None:
        if (
            self.cards[0].left < x < self.cards[-1].right and
            self.cards[0].bottom < y < self.cards[-1].top
        ):
            for card in self.cards:
                if (
                    card.left < x < card.right and
                    card.bottom < y < card.top
                ):
                    self.set_hover_card(card)
                    break

            self.show_cards = True
            self.view.slow_down = True

        else:
            self.show_cards = False
            self.view.slow_down = False

    def process_mouse_press(self, x, y, button) -> bool:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                self.cards[0].left < x < self.cards[-1].right and
                self.cards[0].bottom < y < self.cards[-1].top
            ):

                for idx, card in enumerate(self.cards):
                    if (
                        card.left < x < card.right and
                        card.bottom < y < card.top
                    ):
                        self.view.player.curr_color = self.colors[idx]
                        self.show_cards = False
                        self.view.slow_down = False

                return True

        return False

    def draw(self) -> None:
        self.cards.draw()

    def update(self, delta_time: float = 1/60):
        viewport = (self.view.camera.viewport_left, self.view.camera.viewport_bottom)

        if self.prev_viewport != viewport:
            for card in self.cards:
                card.center_x += viewport[0] - self.prev_viewport[0]
                card.center_y += viewport[1] - self.prev_viewport[1]

            self.prev_viewport = viewport

        max_hover_height = self.MAX_CARD_HOVER_HEIGHT + viewport[1]
        max_height = self.MAX_CARD_HEIGHT + viewport[1]
        min_height = self.MIN_CARD_HEIGHT + viewport[1]

        for card in self.cards:
            max_card_height = max_hover_height if card == self.hover_card else max_height

            if (
                self.show_cards and
                card == self.prev_hover_card and
                card.center_y >= max_height
            ):
                card.change_y = -10

            elif (
                (self.show_cards and card.center_y >= max_card_height) or
                (not self.show_cards and card.center_y <= min_height)
            ):
                card.change_y = 0

            elif card == self.prev_hover_card:
                self.prev_hover_card = None

            elif self.show_cards:
                card.change_y = 10

            else:
                card.change_y = -10

        self.cards.update()
