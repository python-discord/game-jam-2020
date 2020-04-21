import math
import os
import pymunk.pygame_util
import itertools
from gamer_gang.mobs import *
from gamer_gang.terrainStuff import *

SCALE = 1
OFFSCREEN_SPACE = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Triple Blocks"
SCREEN_MARGIN = 200


class ActualGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcade.set_background_color(arcade.color.BLUE)

    def setup(self):
        self.frames = 0
        self.total_time = 0
        self.game_over = False
        self.debugging = False
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.view_left = self.view_bottom = 0
        self.timeAfterSplit = 0
        self.controlled = 0
        self.key_pressed = [0, 0, 0]  # the user input

        self.normalGrounds = arcade.SpriteList()
        self.spikes = arcade.SpriteList()
        self.players = []
        self.shapes = []

        self.normalGroundTextures = [arcade.load_texture("images/ground/placeholderGround.png")]
        self.playerTextures = [[arcade.load_texture("images/mobs/player/1.png")],
                               [arcade.load_texture("images/mobs/player/2.png")],
                               [arcade.load_texture("images/mobs/player/3.png")]]

        self.bodies = []
        for i in range(1, 4):
            p, body, shape = makeMob(1, self.space, Player, self.playerTextures[i - 1], 1, 32 * (i + 3), 32, str(i))
            self.bodies.append(body)
            self.shapes.append(shape)
            self.players.append(p)
            self.playerHeight = p.height

        for i in range(20):
            g = makeTerrain(self.space, NormalGround, self.normalGroundTextures, 10, i * 32, 0)
            self.normalGrounds.append(g)

        for i in range(1):
            pass

    def on_draw(self):
        arcade.start_render()

        self.normalGrounds.draw()
        for p in self.players:
            p.draw()

        if self.debugging:
            for i in self.players:
                i.draw_hit_box((100, 100, 100), 3)
            for i in self.normalGrounds:
                i.draw_hit_box((100, 100, 100))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_pressed[1] = -20
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_pressed[0] = 20
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_pressed[2] = 500
        elif key == arcade.key.NUM_1 or key == arcade.key.KEY_1:
            self.controlled = 0
        elif key == arcade.key.NUM_2 or key == arcade.key.KEY_2:
            self.controlled = 1
        elif key == arcade.key.NUM_3 or key == arcade.key.KEY_3:
            self.controlled = 2
        elif key == arcade.key.DOWN:
            self.splitStack()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_pressed[1] = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_pressed[0] = 0
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN:
            self.key_pressed[2] = 0

    def cameraShift(self):
        needChange = False
        left_boundary = self.view_left + SCREEN_MARGIN
        if self.players[self.controlled].left < left_boundary:
            self.view_left -= left_boundary - self.players[self.controlled].left
            needChange = True

        right_boundary = self.view_left + SCREEN_WIDTH - SCREEN_MARGIN
        if self.players[self.controlled].right > right_boundary:
            self.view_left += self.players[self.controlled].right - right_boundary
            needChange = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - SCREEN_MARGIN
        if self.players[self.controlled].top > top_boundary:
            self.view_bottom += self.players[self.controlled].top - top_boundary
            needChange = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        if needChange:
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left - 1,
                                self.view_bottom, SCREEN_HEIGHT + self.view_bottom - 1)

    def stackCheck(self):
        if self.timeAfterSplit < 0.5:  # don't join right after the user tells the blocks to split
            return

        for up, down in itertools.permutations(self.players, 2):
            if up.name != down.name:
                if abs(up.bottom - down.top) < 5 and abs(up.center_x - down.center_x) < 10:
                    stackName = f'{up.name}on{down.name}'
                    stackList = []
                    for v, p in enumerate(self.players):
                        if p.name in [up.name, down.name]:
                            stackList.append(v)

                    p, body, shape = makeMob(1, self.space, Player,
                                             [arcade.load_texture(f'images/mobs/player/{stackName}.png')],
                                             1, down.center_x, (down.bottom + up.top) / 2, stackName)

                    for i in stackList:
                        self.players[i].kill()  # remove ALL TRACES of the prev sprites
                        try:
                            self.space.remove(self.bodies[i], self.shapes[i])
                        except KeyError:  # no idea why this crap happens
                            pass
                        self.players[i], self.bodies[i], self.shapes[i] = p, body, shape

                    break  # break bc we can only have 2 things join at a time, right?

    def splitStack(self):
        if len(self.players) == len(set(self.players)):  # nothing's joined, so wut you talking about
            return

        for p in self.players:
            if str(self.controlled + 1) in p.name:
                presentIndexes = [int(i) - 1 for i in p.name.split(sep='on')]
                topList = presentIndexes[:presentIndexes.index(self.controlled) + 1]
                bottomList = presentIndexes[presentIndexes.index(self.controlled) + 1:]
                bottom = p.bottom  # it's a constant, so the top and the bottom don't affect each other
                if not bottomList:
                    return
                # configure top part of the stack (p, b, s stand for player, body, and shape respectively)
                topListName = "on".join([str(s + 1) for s in topList])
                p, b, s = makeMob(1, self.space, Player,
                                  [arcade.load_texture(f'images/mobs/player/{topListName}.png')],
                                  1, p.center_x, bottom + self.playerHeight * (len(bottomList) + len(topList) / 2),
                                  topListName)

                for i in topList:  # actually put the newly split sprites in the game
                    self.players[i].kill()
                    try:
                        self.space.remove(self.bodies[i], self.shapes[i])
                    except KeyError:
                        pass
                    self.players[i], self.bodies[i], self.shapes[i] = p, b, s

                # do the same for the bottom part
                bottomListName = "on".join([str(s + 1) for s in bottomList])
                p, b, s = makeMob(1, self.space, Player,
                                  [arcade.load_texture(f'images/mobs/player/{bottomListName}.png')],
                                  1, p.center_x, bottom + self.playerHeight * (len(bottomList) / 2), bottomListName)

                for i in bottomList:
                    self.players[i].kill()
                    try:
                        self.space.remove(self.bodies[i], self.shapes[i])
                    except KeyError:
                        pass
                    self.players[i], self.bodies[i], self.shapes[i] = p, b, s
                self.key_pressed[2] = 500
                self.timeAfterSplit = 0
                break

    def movement(self):
        for p in self.players:
            if p.name == self.players[self.controlled].name:
                p.pymunk_shape.body.velocity += pymunk.Vec2d((sum(self.key_pressed[:2]), 0))  # hor. movement
                if p.can_jump:
                    p.pymunk_shape.body.velocity += pymunk.Vec2d((0, self.key_pressed[2]))
                    p.can_jump = False

                if p.pymunk_shape.body.velocity.x > 300:  # prevent from accelerating too fast
                    p.pymunk_shape.body.velocity = pymunk.Vec2d((150, p.pymunk_shape.body.velocity.y))

                if p.pymunk_shape.body.velocity.x < -300:
                    p.pymunk_shape.body.velocity = pymunk.Vec2d((-150, p.pymunk_shape.body.velocity.y))

    def entityInteractionCheck(self):
        for p in self.players:
            pass

    def on_update(self, dt):
        self.frames += 1
        self.timeAfterSplit += dt
        self.space.step(1 / 60.0)

        self.movement()  # move all the players (well, the characters)
        self.cameraShift()  # shift camera
        self.stackCheck()  # join into stacks if detected
        self.entityInteractionCheck()  # check for interaction with any enemies, bad stuff, etc.

        for p in self.players:
            if p.top < -100:
                self.game_over = True

        if not self.game_over:
            for i in self.normalGrounds:
                i.update()
            for p in self.players:
                p.update()
                boxes = arcade.check_for_collision_with_list(p, self.normalGrounds)
                if_collide = [True for pl in self.players if arcade.check_for_collision(p, pl) and pl != p]
                if (boxes != [] or True in if_collide) and abs(p.pymunk_shape.body.velocity.y) < 3:
                    p.can_jump = True

            for p in self.players:
                p.center_x = p.pymunk_shape.body.position.x
                p.center_y = p.pymunk_shape.body.position.y
                p.angle = math.degrees(p.pymunk_shape.body.angle)

        else:  # TODO: implement a game over/restart screen
            self.close()


def main():
    window = ActualGame()
    window.setup()
    arcade.run()


main()
