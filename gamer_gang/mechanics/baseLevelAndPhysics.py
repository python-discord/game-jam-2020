import math
import itertools
from gamer_gang.mechanics.mobs import *
from gamer_gang.mechanics.terrainStuff import *
from gamer_gang.dumbConstants import *

def getNames(name):
    name = name.split(sep='on')
    frontier = [[]]
    for _ in range(len(name)):
        inLine = []
        for n in frontier:
            inLine.extend([n + [0], n + [1]])
        frontier = inLine
    newNames = []
    for n in frontier:
        new = ''
        for i in range(len(name)):
            new += 'other' + name[i] + 'on' if n[i] else name[i] + 'on'
        newNames.append(new[:-2])

    return newNames

class BaseLevel(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_show(self):
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        self.frames = 0
        self.total_time = 0
        self.debugging = False
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.leftView = self.bottomView = 0
        self.timeAfterSplit = 0
        self.controlled = 0
        self.userInputs = [0, 0, 0]  # the user input
        self.deathCause = None

        self.normalGrounds = arcade.SpriteList()
        self.spikes = arcade.SpriteList()
        self.goombaThings = arcade.SpriteList()
        self.players = []
        self.shapes = []

        self.normalGroundTextures = [arcade.load_texture("images/ground/placeholderGround.png")]
        self.spikeTextures = [arcade.load_texture('images/ground/spike.png')]
        self.playerTextures = [[arcade.load_texture("images/mobs/player/1.png"),
                                arcade.load_texture("images/mobs/player/other1.png")],
                               [arcade.load_texture("images/mobs/player/1.png"),
                                arcade.load_texture("images/mobs/player/other3.png")],
                               [arcade.load_texture("images/mobs/player/1.png"),
                                arcade.load_texture("images/mobs/player/other2.png")]]
        self.enemyTextures = [arcade.load_texture('images/mobs/goombaThing/goomba1.png'),
                              arcade.load_texture('images/mobs/goombaThing/goomba1.png')]

        self.bodies = []
        self.make_level()

    def make_level(self):  # in the base class, this is just a placeholder level
        for i in range(1, 4):
            p, body, shape = makePlayer(1, self.space, self.playerTextures[i - 1], 1, 17, 32 * i, str(i))
            self.bodies.append(body)
            self.shapes.append(shape)
            self.players.append(p)
            self.playerHeight = p.height

        for i in range(40):
            self.normalGrounds.append(makeTerrain(self.space, NormalGround, self.normalGroundTextures, 1, i * 32, 0))

        for i in range(1):
            self.spikes.append(makeTerrain(self.space, BadSpike, self.spikeTextures, 1, 200, 20))

        for i in range(1):
            self.goombaThings.append(makeEnemy(1, self.space, self.enemyTextures, 1, 150, 30, -1))

    def on_draw(self):
        arcade.start_render()

        self.spikes.draw()
        self.normalGrounds.draw()
        self.goombaThings.draw()
        for p in self.players:
            p.draw()

        if self.debugging:
            for i in self.players:
                i.draw_hit_box((100, 100, 100), 3)
            for f in self.normalGrounds:
                f.draw_hit_box((100, 100, 100), 3)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.userInputs[1] = -20
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.userInputs[0] = 20
        elif key == arcade.key.UP or key == arcade.key.W:
            self.userInputs[2] = 500
        elif key == arcade.key.NUM_1 or key == arcade.key.KEY_1:
            self.controlled = 0
        elif key == arcade.key.NUM_2 or key == arcade.key.KEY_2:
            self.controlled = 1
        elif key == arcade.key.NUM_3 or key == arcade.key.KEY_3:
            self.controlled = 2
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.splitStack()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.userInputs[1] = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.userInputs[0] = 0
        elif key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN:
            self.userInputs[2] = 0

    def cameraShift(self):
        needChange = False
        left_boundary = self.leftView + SCREEN_MARGIN
        if self.players[self.controlled].left < left_boundary:
            self.leftView -= left_boundary - self.players[self.controlled].left
            needChange = True

        right_boundary = self.leftView + SCREEN_WIDTH - SCREEN_MARGIN
        if self.players[self.controlled].right > right_boundary:
            self.leftView += self.players[self.controlled].right - right_boundary
            needChange = True

        top_boundary = self.bottomView + SCREEN_HEIGHT - SCREEN_MARGIN
        if self.players[self.controlled].top > top_boundary:
            self.bottomView += self.players[self.controlled].top - top_boundary
            needChange = True

        bottom_boundary = self.bottomView + SCREEN_MARGIN
        if self.players[self.controlled].bottom < bottom_boundary:
            self.bottomView -= bottom_boundary - self.players[self.controlled].bottom
            needChange = True

        self.leftView = round(self.leftView)
        self.bottomView = round(self.bottomView)

        if needChange:
            arcade.set_viewport(self.leftView, SCREEN_WIDTH + self.leftView,
                                self.bottomView, SCREEN_HEIGHT + self.bottomView)

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

                    possTextures = [arcade.load_texture(f'images/mobs/player/{n}.png') for n in getNames(stackName)]
                    p, body, shape = makePlayer(1, self.space, possTextures,
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
                possTextures = [arcade.load_texture(f'images/mobs/player/{n}.png') for n in getNames(topListName)]
                p, b, s = makePlayer(1, self.space, possTextures, 1,
                                     p.center_x, bottom + self.playerHeight * (len(bottomList) + len(topList) / 2),
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
                possTextures = [arcade.load_texture(f'images/mobs/player/{n}.png') for n in getNames(bottomListName)]
                p, b, s = makePlayer(1, self.space, possTextures, 1, p.center_x,
                                     bottom + self.playerHeight * (len(bottomList) / 2), bottomListName)

                for i in bottomList:
                    self.players[i].kill()
                    try:
                        self.space.remove(self.bodies[i], self.shapes[i])
                    except KeyError:
                        pass
                    self.players[i], self.bodies[i], self.shapes[i] = p, b, s
                self.userInputs[2] = 500
                self.timeAfterSplit = 0
                break

    def movement(self):
        for p in self.players:
            if p.name == self.players[self.controlled].name:
                p.pymunk_shape.body.velocity += pymunk.Vec2d((sum(self.userInputs[:2]), 0))  # hor. movement
                if p.can_jump:
                    p.pymunk_shape.body.velocity += pymunk.Vec2d((0, self.userInputs[2]))
                    p.can_jump = False

                if p.pymunk_shape.body.velocity.x > 300:  # prevent from accelerating too fast
                    p.pymunk_shape.body.velocity = pymunk.Vec2d((150, p.pymunk_shape.body.velocity.y))

                if p.pymunk_shape.body.velocity.x < -300:
                    p.pymunk_shape.body.velocity = pymunk.Vec2d((-150, p.pymunk_shape.body.velocity.y))

    def entityInteractionCheck(self):
        for p in self.players:
            if arcade.check_for_collision_with_list(p, self.spikes):  # if you touch a spike, you DIE
                self.window.game_over = True  # and you GO TO HELL ALONG WITH PYTHON 2
                self.deathCause = 'you got impaled by a spike that looks awfully like a GD spike'

            for e in self.goombaThings:
                if arcade.check_for_collision(p, e):
                    print(abs(p.bottom - e.top))
                    if abs(p.bottom - e.top) < 3:
                        e.kill()
                        p.pymunk_shape.body.velocity += pymunk.Vec2d((0, 400))
                        continue
                    self.window.game_over = True
                    self.deathCause = 'you got oofed by some random enemy, stupid i know right?'

    def on_update(self, dt):
        self.frames += 1
        self.timeAfterSplit += dt
        for _ in range(10):
            self.space.step(1 / 600.0)

        self.movement()  # move all the players (well, the characters)
        self.cameraShift()  # shift camera
        self.stackCheck()  # join into stacks if detected
        self.entityInteractionCheck()  # check for interaction with any enemies, bad stuff, etc.

        for p in self.players:
            if p.top < -100:
                self.window.game_over = True
                self.deathCause = 'no pit is more bottomless than the bottomless pit! (which you fell into)'

        if not self.window.game_over:
            self.goombaThings.update()
            self.goombaThings.update_animation(dt)
            for p in self.players:
                p.update()
                p.update_animation(dt)
                boxes = arcade.check_for_collision_with_list(p, self.normalGrounds)
                if_collide = [True for pl in self.players if arcade.check_for_collision(p, pl) and pl != p]
                if (boxes != [] or True in if_collide) and abs(p.pymunk_shape.body.velocity.y) < 3:
                    p.can_jump = True

            for p in self.players:
                p.center_x = p.pymunk_shape.body.position.x
                p.center_y = p.pymunk_shape.body.position.y
                p.angle = math.degrees(p.pymunk_shape.body.angle)

        else:
            self.window.show_view(self.window.gameOver)
