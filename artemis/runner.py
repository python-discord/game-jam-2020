import arcade
import random
import pymunk
import math


BLOCKS_Y = 20
BLOCKS_X = 40
SCALING = 0.25
HEIGHT = int(BLOCKS_Y * SCALING * 128)
WIDTH = int(BLOCKS_X * SCALING * 128)
SIDE = int(128 * SCALING)

SPEED = 20 * SCALING
JUMP = 45 * SCALING
FRICTION = 0.1
GRAVITY = 10 * SCALING


class BiDirectionalPhysicsEnginePlatformer(arcade.PhysicsEnginePlatformer):
    def can_jump(self, y_distance=5):
        if self.gravity_constant > 0:
            return super().can_jump()

        self.player_sprite.center_y += y_distance
        hit_list = arcade.physics_engines.check_for_collision_with_list(
            self.player_sprite, self.platforms
        )
        self.player_sprite.center_y -= y_distance

        if len(hit_list) > 0:
            self.jumps_since_ground = 0

        if (
                len(hit_list) > 0 or self.allow_multi_jump
                and self.jumps_since_ground < self.allowed_jumps
                ):
            return True
        else:
            return False


class Player(arcade.Sprite):
    TEXTURES = [
        'jump_0', 'jump_1', 'jump_2', 'jump_3', 'walk_forward',
        'walk_right_0', 'walk_right_1', 'walk_right_2', 'walk_right_3',
        'walk_forward_u', 'walk_right_0_u', 'walk_right_1_u',
        'walk_right_2_u', 'walk_right_3_u'
    ]

    def __init__(
            self, game, x=WIDTH//5, y=HEIGHT//2, speed=SPEED, jump=JUMP,
            image='artemis/assets/player_{}.png'
            ):
        super().__init__(
            image.format('walk_right_0'), center_x=x, center_y=y, 
            scale=SCALING*0.25
        )
        self.image = image
        self.textures = []
        for texture in Player.TEXTURES:
            self.textures.append(arcade.load_texture(
                image.format(texture)
            ))
        self.scale = SCALING * 0.25
        self.game = game
        self.speed = speed
        self.jump = jump
        self.time_since_change = 0
        self.num = 0
        self.cooldown = 1

    def can_move(self):
        return True

    def update(self, timedelta):
        self.cooldown -= timedelta
        # check touching sprites
        gems = arcade.check_for_collision_with_list(self, self.game.gems)
        for gem in gems:
            gem.remove_from_sprite_lists()

        # check key presses
        if arcade.key.SPACE in self.game.pressed:
            if not self.change_y and self.cooldown < 0:
                if self.game.engine.can_jump():
                    self.game.engine.gravity_constant *= -1
                    self.cooldown = 1

        if self.can_move():
            self.change_x = self.speed

        self.time_since_change += timedelta
        if self.time_since_change > 0.1:
            self.time_since_change = 0
            self.num += 1
            self.num %= 4

        if not self.can_move():
            name = 'walk_forward'
        elif self.game.engine.can_jump():
            name = f'walk_right_{self.num}'
            if self.game.engine.gravity_constant < 0:
                name += '_u'
        else:
            name = f'jump_{self.num}'
        self.texture = self.textures[Player.TEXTURES.index(name)]


class Block(arcade.Sprite):
    def __init__(self, game, x, y, image='artemis/assets/block.png'):
        super().__init__(image, center_x=x, center_y=y, scale=SCALING*1)
        self.game = game
        game.blocks.append(self)

    def update(self):
        if self.center_x < self.game.left-SIDE:
            self.center_x += + WIDTH + SIDE*2


class Gem(arcade.Sprite):
    def __init__(self, game, image='artemis/assets/gem_{}.png'):
        self.value = random.randrange(50, 125)
        col = random.choice('rbyw')
        image = image.format(col)
        super().__init__(image, SCALING * 0.25)
        self.game = game
        game.gems.append(self)
        self.reposition()

    def reposition(self):
        self.center_x = (random.randrange(BLOCKS_X)+0.5) * SCALING * 128
        self.center_y = (random.randrange(BLOCKS_Y)+0.5) * SCALING * 128

    def update(self):
        for others in (self.game.blocks, self.game.gems):
            if arcade.check_for_collision_with_list(self, others):
                self.reposition()


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, 'Runner')
        arcade.set_background_color((25, 0, 50))

        # sprites
        self.player = Player(self)

        self.blocks = arcade.SpriteList()

        # map1 = arcade.tilemap.read_tmx('artemis/maps/map1.tmx')
        # self.blocks = arcade.tilemap.process_layer(map1, 'main', SCALING*4)

        size = int(128 * SCALING)
        for x in range(-SIDE, WIDTH+SIDE, size):
            Block(self, x, size//2)
            Block(self, x, HEIGHT - size//2)

        self.gems = arcade.SpriteList()
        for _ in range(20):
            Gem(self)
        
        self.engine = BiDirectionalPhysicsEnginePlatformer(
            self.player, self.blocks, 1
        )

        # keep track of things
        self.pressed = []
        self.left = 0

        arcade.run()

    def on_draw(self):
        arcade.start_render()
        self.blocks.draw()
        self.gems.draw()
        self.player.draw()

    def on_update(self, timedelta):
        self.gems.update()
        self.blocks.update()
        self.player.update(timedelta)
        self.engine.update()
        self.scroll()

    def scroll(self):
        self.left += self.player.speed
        arcade.set_viewport(self.left, WIDTH + self.left, 0, HEIGHT)

    def on_key_press(self, key, modifiers):
        self.pressed.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.pressed:
            self.pressed.remove(key)


Game()
