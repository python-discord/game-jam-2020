import arcade
import random
import math

from constants import WIDTH, HEIGHT, SCALING, SIDE, TOP, BACKGROUND
from engine import BiDirectionalPhysicsEnginePlatformer
from player import Player
from sprites import Block, Gem
from displays import Box
import views


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(BACKGROUND)

        # sprites
        self.player = Player(self)

        self.blocks = arcade.SpriteList()

        size = int(128 * SCALING)
        for x in range(-SIDE, WIDTH+SIDE, size):
            Block(self, x, HEIGHT - TOP)
            Block(self, x, size//2)

        self.gems = arcade.SpriteList()
        for _ in range(2):
            Gem(self)

        self.boxes = arcade.SpriteList()
        for n in range(5):
            Box(self, n)

        self.others = arcade.SpriteList()
        
        self.engine = BiDirectionalPhysicsEnginePlatformer(
            self.player, self.blocks, 1
        )

        # keep track of things
        self.pressed = []
        self.left = 0
        self.score = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            text=f'Score: {self.score}', start_x=self.left + WIDTH - 50,
            start_y=HEIGHT - (TOP - self.blocks[0].height//2)//2,
            color=arcade.color.WHITE, font_size=20, anchor_x='right',
            anchor_y='center'
        )
        self.blocks.draw()
        self.gems.draw()
        self.boxes.draw()
        self.others.draw()
        self.player.draw()

    def on_update(self, timedelta):
        self.gems.update()
        self.blocks.update()
        self.player.update(timedelta)
        self.boxes.update()
        self.others.update()
        self.engine.update()
        self.scroll()

    def gem_added(self):
        colours = [box.colour for box in self.boxes if box.colour]
        counts = {'r': 0, 'b': 0, 'y': 0}
        for colour in colours:
            if colour == 'w':
                for key in counts:
                    counts[key] += 1
            else:
                counts[colour] += 1
        all_three = None
        for colour in counts:
            if counts[colour] >= 3:
                all_three = colour
        if all_three:
            self.score += 1
            self.remove_three(all_three)
        elif len(colours) == 5:
            self.game_over()

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

    def game_over(self):
        self.window.show_view(views.GameOver('Inventory Full'))

    def scroll(self):
        self.left += self.player.speed
        arcade.set_viewport(self.left, WIDTH + self.left, 0, HEIGHT)

    def on_key_press(self, key, modifiers):
        self.pressed.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.pressed:
            self.pressed.remove(key)