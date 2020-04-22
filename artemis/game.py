import arcade
import random
import math

from constants import WIDTH, HEIGHT, SCALING, SIDE, TOP, BACKGROUND, FONT
from engine import BiDirectionalPhysicsEnginePlatformer
from player import Player
from sprites import Block, Gem, RandomBlock
from displays import Box, PausePlay
from scores import get_hiscore, add_score
from ui import View
import views


class Game(View):
    reset_viewport = False

    def __init__(self):
        super().__init__()
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.set_background_color(BACKGROUND)

        self.left = 0
        self.score = 0
        self.hiscore = get_hiscore()
        self.paused = False
        self.pause_screen = None
        self.blocks = arcade.SpriteList()
        self.gems = arcade.SpriteList()
        self.boxes = arcade.SpriteList()
        self.others = arcade.SpriteList()
        self.spikes = arcade.SpriteList()

        # sprites
        self.player = Player(self)

        size = int(128 * SCALING)
        for x in range(-SIDE, WIDTH+SIDE, size):
            Block(self, x, HEIGHT - TOP, False)
            Block(self, x, size//2, True)

        for _ in range(3):
            Gem(self)
            RandomBlock(self)

        for n in range(5):
            Box(self, n)

        self.pauseplay = PausePlay(0, HEIGHT - 40, self)
        self.buttons.append(self.pauseplay)
        
        self.engine = BiDirectionalPhysicsEnginePlatformer(
            self.player, self.blocks, 1
        )

        self.sprite_lists = [
            self.blocks, self.gems, self.boxes, self.others, self.spikes
        ]

    def on_draw(self):
        arcade.start_render()
        self.pauseplay.center_x = self.left + WIDTH - 40
        super().on_draw()
        arcade.draw_text(
            text=f'High Score: {self.hiscore:03d}',
            start_x=self.left + WIDTH - 100,
            start_y=HEIGHT - (TOP - self.blocks[0].height//2)//2 + 15,
            color=arcade.color.WHITE, font_size=20, anchor_x='right',
            anchor_y='center', font_name=FONT.format('b')
        )
        arcade.draw_text(
            text=f'Score: {self.score:03d}',
            start_x=self.left + WIDTH - 100,
            start_y=HEIGHT - (TOP - self.blocks[0].height//2)//2 - 15,
            color=arcade.color.WHITE, font_size=20, anchor_x='right',
            anchor_y='center', font_name=FONT.format('b')
        )
        for sprite_list in self.sprite_lists:
            sprite_list.draw()
        self.player.draw()
        if self.paused:
            arcade.draw_lrtb_rectangle_filled(
                left=self.left, right=WIDTH+self.left, top=HEIGHT, bottom=0,
                color=(255, 255, 255, 100)
            )
            super().on_draw()
            if not self.pause_screen:
                self.pause_screen = views.Paused(self)
                self.window.show_view(self.pause_screen)

    def on_update(self, timedelta):
        super().on_update(timedelta)
        if not self.paused:
            for sprite_list in self.sprite_lists:
                sprite_list.update()
            self.player.update(timedelta)
            self.engine.update()
            self.scroll()

    def gem_added(self):
        colours = [box.colour for box in self.boxes if box.colour]
        counts = {'r': 0, 'b': 0, 'y': 0}
        for colour in colours:
            if colour == 'w':
                for key in counts:
                    counts[key] += 1
            elif colour in counts:
                counts[colour] += 1
        all_three = None
        for colour in counts:
            if counts[colour] >= 3:
                all_three = colour
        if all_three:
            self.score += 1
            self.remove_three(all_three)
            return
        over = False
        size = 5 - colours.count('p')
        unique = sum(1 for i in 'rby' if (i in colours))
        if len(colours) == 5:
            over = True
        elif size < 3:
            over = True
        elif size - unique < 2:
            over = True
        if over:
            self.game_over('Inventory Full')

    def remove_three(self, colour):
        removed = 0
        for box in self.boxes:
            if box.colour == colour:
                box.remove_gem()
                removed += 1
                if removed == 3:
                    return
        for box in self.boxes:
            if box.colour == 'w':
                box.remove_gem()
                removed += 1
                if removed == 3:
                    return
        assert False, 'Should not get here.'

    def game_over(self, message):
        add_score(self.score)
        self.window.show_view(views.GameOver(message))

    def scroll(self):
        self.left += self.player.speed
        arcade.set_viewport(self.left, WIDTH + self.left, 0, HEIGHT)
        if self.left > self.player.right:
            self.game_over('Got Stuck')

    def on_key_press(self, key, modifiers):
        if not self.paused:
            self.player.switch()
