import math
import itertools
from pathlib import Path
import pytiled_parser
from gamer_gang.mechanics.entities import *
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


def getLayer(layer_path, map_object):
    def _get_tilemap_layer(path, layers):
        layer_name = path.pop(0)
        for layer in layers:
            if layer.name.lower() == layer_name.lower():
                if isinstance(layer, pytiled_parser.objects.LayerGroup):
                    if len(path) != 0:
                        return _get_tilemap_layer(path, layer.layers)
                else:
                    return layer
        return None

    path = layer_path.strip('/').split('/')
    layer = _get_tilemap_layer(path, map_object.layers)
    return layer


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

        self.makeLevel()

    def makeLevel(self):  # the placeholder level here is just level 1
        self.map = arcade.tilemap.read_tmx(str(Path(__file__).parent) + '/levels/level1/level_1.tmx')
        self.ground = arcade.SpriteList()
        self.deco = arcade.SpriteList()
        self.boxes = arcade.SpriteList()
        self.BEES = arcade.SpriteList()
        self.players = []
        self.bodies = []
        self.shapes = []
        self.backgroundImage = arcade.Sprite(str(Path(__file__).parent) + "/levels/level1/blueBackground.png",
                                             center_x=self.map.map_size.width * self.map.tile_size.width / 2,
                                             center_y=self.map.map_size.height * self.map.tile_size.height / 2)
        self.deco = arcade.SpriteList()
        self.score = 0
        self.gotToExit = []  # the players that have gotten to the exit

        ground_list = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/Ground", self.map))
        for i in ground_list:
            self.ground.append(makeLand(self.space, BoxOfSmth, i.textures, 1, i.center_x, i.center_y))

        pName = 1
        for i in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/Players", self.map)):
            p, body, shape = makePlayer(1, self.space, i.textures, 1, i.center_x, i.center_y, str(pName))
            self.bodies.append(body)
            self.shapes.append(shape)
            self.players.append(p)
            self.playerHeight = p.height
            pName += 1

        for b in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/boxes", self.map)):
            box = makeBox(1, self.space, b.textures, b.hit_box, b.scale, b.center_x, b.center_y)
            self.boxes.append(box)

        for b in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/bees", self.map)):
            self.BEES.append(BeeSprite(b.textures, b.scale, b.center_x, b.center_y))

        self.spikes = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/spikes", self.map))
        self.jumpPads = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/jumping pads", self.map))
        self.stars = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/stars", self.map))
        self.exit = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/exit door", self.map))

        self.deco.extend(arcade.tilemap._process_tile_layer(self.map, getLayer("DecorationsBack/Signs", self.map)))
        self.deco.extend(arcade.tilemap._process_tile_layer(self.map, getLayer("DecorationsBack/Trees", self.map)))
        self.deco.extend(arcade.tilemap._process_tile_layer(self.map, getLayer("DecorationsBack/Plants", self.map)))
        self.backgroundSprites = arcade.tilemap._process_tile_layer(self.map,
                                                                    getLayer("DecorationsBack/Ocean", self.map))

    def on_draw(self):
        arcade.start_render()

        self.backgroundImage.draw()
        self.backgroundSprites.draw()
        self.deco.draw()
        self.spikes.draw()
        self.BEES.draw()
        self.ground.draw()
        self.boxes.draw()
        self.jumpPads.draw()
        self.exit.draw()
        self.stars.draw()

        for p in self.players:
            if p is not None:
                p.draw()

        if self.debugging:
            for i in self.players:
                i.draw_hit_box((100, 100, 100), 3)
            for f in self.ground:
                f.draw_hit_box((100, 100, 100), 3)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.userInputs[1] = -30
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.userInputs[0] = 30
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
        self.bottomView = round(self.bottomView) if self.bottomView > 0 else 0

        if needChange:
            arcade.set_viewport(self.leftView, SCREEN_WIDTH + self.leftView,
                                self.bottomView, SCREEN_HEIGHT + self.bottomView)

    def stackCheck(self):
        if self.timeAfterSplit < 0.5:  # don't join right after the user tells the blocks to split
            return

        for up, down in itertools.permutations(self.players, 2):
            if up is not None and down is not None and up.name != down.name:
                if abs(up.bottom - down.top) < 5 and abs(up.center_x - down.center_x) < 10:
                    stackName = f'{up.name}on{down.name}'
                    stackList = []
                    for v, p in enumerate(self.players):
                        if p is not None and p.name in [up.name, down.name]:
                            stackList.append(v)

                    possTextures = [arcade.load_texture(str(Path(__file__).parent) + f'/playerImages/{n}.png')
                                    for n in getNames(stackName)]
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
            if p is not None and str(self.controlled + 1) in p.name:
                presentIndexes = [int(i) - 1 for i in p.name.split(sep='on')]
                topList = presentIndexes[:presentIndexes.index(self.controlled) + 1]
                bottomList = presentIndexes[presentIndexes.index(self.controlled) + 1:]
                bottom = p.bottom  # it's a constant, so the top and the bottom don't affect each other
                if not bottomList:
                    return
                # configure top part of the stack (p, b, s stand for player, body, and shape respectively)
                topListName = "on".join([str(s + 1) for s in topList])
                possTextures = [arcade.load_texture(str(Path(__file__).parent) + f'/playerImages/{n}.png')
                                for n in getNames(topListName)]
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
                possTextures = [arcade.load_texture(str(Path(__file__).parent) + f'/playerImages/{n}.png')
                                for n in getNames(bottomListName)]
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
            if p is None:
                continue

            if p.name == self.players[self.controlled].name:
                p.pymunk_shape.body.velocity += pymunk.Vec2d((sum(self.userInputs[:2]), 0))  # horizontal movement
                if p.can_jump:
                    if arcade.check_for_collision_with_list(p, self.jumpPads):
                        p.pymunk_shape.body.velocity += pymunk.Vec2d((0, 600))
                    else:
                        p.pymunk_shape.body.velocity += pymunk.Vec2d((0, self.userInputs[2]))
                    p.can_jump = False

                if p.pymunk_shape.body.velocity.x > 300:  # prevent from accelerating too fast
                    p.pymunk_shape.body.velocity = pymunk.Vec2d((150, p.pymunk_shape.body.velocity.y))

                if p.pymunk_shape.body.velocity.x < -300:
                    p.pymunk_shape.body.velocity = pymunk.Vec2d((-150, p.pymunk_shape.body.velocity.y))

    def entityInteractionCheck(self):
        for p in self.players:
            if p is None:
                continue

            if arcade.check_for_collision_with_list(p, self.spikes):  # if you touch a spike, you DIE
                #self.window.game_over = True  # and you GO TO HELL ALONG WITH PYTHON 2
                self.deathCause = 'a spike that looks awfully like a GD spike'
                continue

            if arcade.check_for_collision_with_list(p, self.BEES):
                #self.window.game_over = True
                self.deathCause = 'BEEEEEEEEES that most definitely don\'t like jazz ' \
                                  '(and probably aren\'t from animal crossing either)'
                continue

            if arcade.check_for_collision_with_list(p, self.stars):
                for collided in arcade.check_for_collision_with_list(p, self.stars):
                    collided.remove_from_sprite_lists()
                self.score += 1

            left = []
            if arcade.check_for_collision_with_list(p, self.exit):
                for v, pl in enumerate(self.players):
                    if pl == p:
                        self.players[v].kill()
                        try:
                            self.space.remove(self.bodies[v], self.shapes[v])
                        except KeyError:
                            pass
                        self.players[v] = None
                        self.gotToExit.append(v + 1)
                    elif pl is not None:
                        if set([int(c) for c in pl.name.split('on') if c]).intersection(self.gotToExit):
                            continue
                        left.append(v)

                if left:
                    self.controlled = left[0]
                else:
                    self.window.show_view(self.window.menuView)

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
            if p is not None and p.top < -50:
                self.window.game_over = True
                self.deathCause = 'no pit is more bottomless than the bottomless pit! (which you fell into)'

        if not self.window.game_over:
            for p in self.players:
                if p is None:
                    continue

                p.update()
                p.update_animation(dt)
                collidedGround = [g for g in arcade.check_for_collision_with_list(p, self.ground) if p.top > g.bottom]
                collidedBoxes = [b for b in arcade.check_for_collision_with_list(p, self.boxes)
                                 if abs(p.bottom - b.top) < 5]
                metPlayers = [True for pl in self.players if pl is not None and
                              arcade.check_for_collision(p, pl) and pl != p]  # the players that are beneath

                if (collidedGround or metPlayers or collidedBoxes) and abs(p.pymunk_shape.body.velocity.y) < 3:
                    p.can_jump = True

                p.center_x = p.pymunk_shape.body.position.x
                p.center_y = p.pymunk_shape.body.position.y
                p.angle = math.degrees(p.pymunk_shape.body.angle)

            for b in self.boxes:
                b.center_x = b.pymunk_shape.body.position.x
                b.center_y = b.pymunk_shape.body.position.y
                b.angle = math.degrees(b.pymunk_shape.body.angle)
                if b.center_y <= 0:
                    self.space.remove(b.pymunk_shape, b.pymunk_shape.body)
                    b.kill()

            for b in self.BEES:
                b.update(self.players)

        else:
            print(self.deathCause)
            self.window.show_view(self.window.gameOver)


if __name__ == '__main__':
    testGame = arcade.Window(1000, 600, 'test')
    testGame.level = BaseLevel()
    testGame.game_over = False
    testGame.show_view(testGame.level)
    arcade.run()
