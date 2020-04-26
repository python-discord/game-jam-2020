import itertools
from pathlib import Path
import pytiled_parser
from gamer_gang.epicAssets.entities import *
from gamer_gang.epicAssets.terrainStuff import *
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
        for l in layers:
            if l.name.lower() == layer_name.lower():
                if isinstance(l, pytiled_parser.objects.LayerGroup):
                    if len(path) != 0:
                        return _get_tilemap_layer(path, l.layers)
                else:
                    return l
        return None

    path = layer_path.strip('/').split('/')
    layer = _get_tilemap_layer(path, map_object.layers)
    return layer


class Level(arcade.View):
    def __init__(self, levelNum):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.ln = levelNum  # ln stands for level number

    def on_show(self):
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        self.debugging = False
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.leftView = self.bottomView = 0
        self.timeAfterSplit = 0
        self.controlled = 0
        self.userInputs = [0, 0, 0]  # the user input

        self.makeLevel()

    def makeLevel(self):
        self.map = arcade.tilemap.read_tmx(str(Path(__file__).parent) + f'/levels/level_{self.ln}.tmx')
        self.frames = 0
        self.totalTime = 0
        self.ground = arcade.SpriteList()
        self.sands = arcade.SpriteList()
        self.deco = arcade.SpriteList()
        self.boxes = arcade.SpriteList()
        self.BEES = arcade.SpriteList()
        self.stars = arcade.SpriteList()
        self.msg = None
        self.players = []
        self.bodies = []
        self.shapes = []
        self.backgroundImage = arcade.Sprite(str(Path(__file__).parent) + "/levels/blueBackground.png",
                                             center_x=self.map.map_size.width * self.map.tile_size.width / 2,
                                             center_y=self.map.map_size.height * self.map.tile_size.height / 2)
        self.deco = arcade.SpriteList()
        self.collectedStars = 0
        self.gotToExit = []  # the players that have gotten to the exit
        self.gotAllStars = False

        ground_list = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/Ground", self.map))
        for i in ground_list:
            self.ground.append(makeLand(self.space, i.textures, 1, i.center_x, i.center_y))

        pName = 1
        for i in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/Players", self.map)):
            p, body, shape = makePlayer(15, self.space, i.textures, 1, i.center_x, i.center_y, str(pName))
            self.bodies.append(body)
            self.shapes.append(shape)
            self.players.append(p)
            self.playerHeight = p.height
            pName += 1

        for b in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/boxes", self.map)):
            self.boxes.append(makeBox(1, self.space, b.textures, b.hit_box, b.scale, b.center_x, b.center_y))

        try:
            for s in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/sands", self.map)):
                self.sands.append(makeLand(self.space, s.textures, s.scale, s.center_x, s.center_y))
        except AttributeError:
            pass

        try:
            for b in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/bees", self.map)):
                textures = {"f1": [arcade.load_texture(str(Path(__file__).parent) + f"/images/beeImages/bee{i}.png")
                                   for i in range(1, 3)],
                            "f2": [arcade.load_texture(str(Path(__file__).parent) + f"/images/beeImages/bee{i}.png",
                                                       mirrored=True) for i in range(1, 3)]}
                self.BEES.append(BeeSprite(textures, b.scale, b.center_x, b.center_y))
        except AttributeError:
            pass

        for s in arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/stars", self.map)):
            self.stars.append(StarSprite(s.textures, 1, s.center_x, s.center_y, s.hit_box))
        self.neededStars = len(self.stars)

        self.spikes = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/spikes", self.map))
        self.jumpPads = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/jumping pads", self.map))
        self.exit = arcade.tilemap._process_tile_layer(self.map, getLayer("Interactions/exit door", self.map))
        self.exit[0].textures = [arcade.load_texture(str(Path(__file__).parent) + '/images/doorImages/doorClosed.png'),
                                 arcade.load_texture(str(Path(__file__).parent) + '/images/doorImages/doorOpen.png')]
        self.exit[0].texture = self.exit[0].textures[0]
        self.exit[0].center_y -= 16

        self.deco.extend(arcade.tilemap._process_tile_layer(self.map, getLayer("DecorationsBack/Trees", self.map)))
        self.deco.extend(arcade.tilemap._process_tile_layer(self.map, getLayer("DecorationsBack/Plants", self.map)))
        self.deco.extend(arcade.tilemap._process_tile_layer(self.map, getLayer("DecorationsBack/Signs", self.map)))
        try:
            self.bkg = arcade.SpriteList()
            self.bkg.extend(arcade.tilemap._process_tile_layer(self.map, getLayer("DecorationsBack/Ocean", self.map)))
        except AttributeError:
            pass

        self.xCam = round(self.players[0].center_x) + random.randint(-SCREEN_WIDTH, SCREEN_WIDTH)
        self.yCam = round(self.players[0].center_y) + random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()

        self.backgroundImage.draw()
        self.bkg.draw()
        self.deco.draw()
        self.exit.draw()
        self.spikes.draw()
        self.BEES.draw()
        self.ground.draw()
        self.boxes.draw()
        self.jumpPads.draw()
        self.sands.draw()
        self.stars.draw()
        if self.msg is not None: self.msg.draw()

        if self.collectedStars != self.neededStars:
            arcade.draw_text(f'stars collected: {self.collectedStars} out of {self.neededStars}',
                             self.xCam - SCREEN_WIDTH / 2 + 10, self.yCam + SCREEN_HEIGHT / 2 - 30,
                             font_size=20, color=arcade.color.BLACK)
        else:
            arcade.draw_text(f'exit unlocked!', self.xCam - SCREEN_WIDTH / 2 + 10, self.yCam + SCREEN_HEIGHT / 2 - 30,
                             font_size=20, color=arcade.color.BLACK)

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

    def cameraShift(self, t):
        self.xCam = round(self.xCam * (1 - t) + self.players[self.controlled].pymunk_shape.body.position.x * t)
        self.xCam = self.xCam if self.xCam >= SCREEN_WIDTH / 2 else SCREEN_WIDTH / 2
        if not self.xCam <= self.map.map_size.width * self.map.tile_size.width - SCREEN_WIDTH / 2:
            self.xCam = self.map.map_size.width * self.map.tile_size.width - SCREEN_WIDTH / 2

        self.yCam = round(self.yCam * (1 - t) + self.players[self.controlled].pymunk_shape.body.position.y * t)
        self.yCam = self.yCam if self.yCam >= SCREEN_HEIGHT / 2 else SCREEN_HEIGHT / 2
        if not self.yCam <= self.map.map_size.height * self.map.tile_size.height - SCREEN_HEIGHT / 2:
            self.yCam = self.map.map_size.height * self.map.tile_size.height - SCREEN_HEIGHT / 2

        arcade.set_viewport(self.xCam - SCREEN_WIDTH / 2, self.xCam + SCREEN_WIDTH / 2,
                            self.yCam - SCREEN_HEIGHT / 2, self.yCam + SCREEN_HEIGHT / 2)

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

                    possTextures = [arcade.load_texture(str(Path(__file__).parent) + f'/images/playerImages/{n}.png')
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
                possTextures = [arcade.load_texture(str(Path(__file__).parent) + f'/images/playerImages/{n}.png')
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
                possTextures = [arcade.load_texture(str(Path(__file__).parent) + f'/images/playerImages/{n}.png')
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
                        self.window.sfx['jump'].play()
                    else:
                        if self.userInputs[2]:
                            p.pymunk_shape.body.velocity += pymunk.Vec2d((0, self.userInputs[2]))
                            self.window.sfx['jump'].play()
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
                self.window.game_over = True  # and you GO TO HELL ALONG WITH PYTHON 2
                self.window.sfx['spike'].play()
                self.window.deathCause = 'a spike that looks awfully like a GD spike'
                continue

            if arcade.check_for_collision_with_list(p, self.BEES):
                self.window.game_over = True
                self.window.sfx['sting'].play()
                self.window.deathCause = 'BEEEEEEEEES that most definitely don\'t like jazz'
                continue

            if arcade.check_for_collision_with_list(p, self.stars):
                for collided in arcade.check_for_collision_with_list(p, self.stars):
                    if not collided.obtained:
                        self.collectedStars += 1
                        self.window.sfx['star'].play()
                        collided.obtained = True

            left = []
            if arcade.check_for_collision_with_list(p, self.exit) and self.collectedStars == self.neededStars:
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
                    self.window.sfx['win'].play()
                    self.window.show_view(self.window.menuView)

    def on_update(self, dt):
        self.frames += 1
        self.timeAfterSplit += dt
        if self.totalTime == 0:
            self.window.sfx["level music"].play(volume=0.3)
        if self.window.sfx["level music"].get_length() < self.totalTime:
            self.totalTime = 0
        else:
            self.totalTime += dt

        for _ in range(10):
            self.space.step(dt/10)

        self.movement()  # move all the players (well, the characters)
        self.cameraShift(dt)  # shift camera
        self.stackCheck()  # join into stacks if detected
        self.entityInteractionCheck()  # check for interaction with any enemies, bad stuff, etc.

        for p in self.players:
            if p is not None and p.top < 0:
                self.window.game_over = True
                self.window.sfx['void'].play()
                self.window.deathCause = 'the bottomless bottomless pit'

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

            spriteListPlayers = arcade.SpriteList()
            for p in self.players:
                if p is not None:
                    spriteListPlayers.append(p)

            newSands = arcade.SpriteList()
            for s in self.sands:
                s.center_x = s.pymunk_shape.body.position.x
                s.center_y = s.pymunk_shape.body.position.y
                s.center_y -= 32
                metBoxes = arcade.check_for_collision_with_list(s, self.boxes)
                metBoxes.extend(arcade.check_for_collision_with_list(s, self.ground))
                metBoxes.extend(arcade.check_for_collision_with_list(s, spriteListPlayers))
                collided = [True for char in self.sands if arcade.check_for_collision(s, char) and s != char]
                if not metBoxes and not collided:
                    newSands.append(makeLand(self.space, s.textures, 1, s.center_x, s.center_y))
                    self.space.remove(s.pymunk_shape, s.pymunk_shape.body)
                    s.kill()
                else:
                    s.center_y += 32
                if s.center_y <= 0:
                    self.space.remove(s.pymunk_shape, s.pymunk_shape.body)
                    s.kill()
            self.sands.extend(newSands)

            self.BEES.update_animation(dt)
            for b in self.BEES:
                b.update(self.players)

            if self.collectedStars == self.neededStars and not self.gotAllStars:
                self.window.sfx["win"].play()
                self.msg = MessagePop(arcade.load_texture(str(Path(__file__).parent) + "/images/doorUnlocked.png"))
                self.exit[0].texture = self.exit[0].textures[1]
                self.gotAllStars = True

            for s in self.stars:
                s.update(self.frames)
                if s.alpha == 0:
                    s.kill()

            if self.msg is not None:
                self.msg.update(self.xCam, self.yCam)
                if self.msg.alpha <= 0:
                    self.msg = None

        else:
            self.window.show_view(self.window.gameOver)


if __name__ == '__main__':
    testGame = arcade.Window(1000, 600, 'test')
    testGame.level = Level(1)
    testGame.game_over = False
    filePath = str(Path(__file__).parent.parent)
    testGame.sfx = {"jump": arcade.load_sound(filePath + "/epicAssets/sounds/jump.wav"),
                    "star": arcade.load_sound(filePath + "/epicAssets/sounds/star.wav"),
                    "void": arcade.load_sound(filePath + "/epicAssets/sounds/dropVoid.wav"),
                    "sting": arcade.load_sound(filePath + "/epicAssets/sounds/beeSting.wav"),
                    "lost": arcade.load_sound(filePath + "/epicAssets/sounds/levelLost.wav"),
                    "win": arcade.load_sound(filePath + "/epicAssets/sounds/levelPass.wav"),
                    "spike": arcade.load_sound(filePath + "/epicAssets/sounds/spike.wav"),
                    "level music": arcade.load_sound(filePath + "/epicAssets/sounds/background.wav"),
                    "menu music": arcade.load_sound(filePath + "/epicAssets/sounds/menu.wav")}
    testGame.show_view(testGame.level)
    arcade.run()
