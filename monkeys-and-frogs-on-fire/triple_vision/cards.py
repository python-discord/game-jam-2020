import arcade

from triple_vision.constants import SCALING, WINDOW_SIZE


class CardManager:

    def __init__(self, ctx) -> None:
        self.ctx = ctx

        self.cards = arcade.SpriteList()
        self.colors = ('red', 'green', 'blue')

        card_scale = SCALING / 6

        self.MIN_CARD_HEIGHT = -132 * card_scale
        self.MAX_CARD_HEIGHT = 84 * card_scale
        self.MAX_CARD_HOVER_HEIGHT = 280 * card_scale

        for idx, color in enumerate(self.colors):
            self.cards.append(
                arcade.Sprite(
                    filename=f'assets/wizard/{color}_card.png',
                    scale=card_scale,
                    center_x=WINDOW_SIZE[0] / 2 + (idx - 1) * 400 * card_scale,
                    center_y=self.MIN_CARD_HEIGHT
                )
            )

        self.show_cards = False
        self.hover_card = None

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
                    self.hover_card = card
                    break

            self.show_cards = True
            self.ctx.paused = True

        else:
            self.show_cards = False
            self.ctx.paused = False

    def check_mouse_press(self, x, y, button) -> bool:
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
                        self.ctx.player.curr_color = self.colors[idx]
                        self.show_cards = False
                        self.ctx.paused = False

                return True

        return False

    def draw(self) -> None:
        self.cards.draw()

    def update(self, delta_time: float = 1/60):
        if not self.show_cards:
            for card in self.cards:
                card.change_y = -10

        elif self.show_cards:
            for card in self.cards:
                card.change_y = 10

        for card in self.cards:
            max_height = self.MAX_CARD_HOVER_HEIGHT \
                if card == self.hover_card else self.MAX_CARD_HEIGHT

            if (
                self.show_cards and
                card != self.hover_card and
                card.center_y >= self.MAX_CARD_HEIGHT
            ):
                card.change_y = -10

            if (
                (self.show_cards and card.center_y >= max_height) or
                (not self.show_cards and card.center_y <= self.MIN_CARD_HEIGHT)
            ):
                card.change_y = 0

        self.cards.update()
