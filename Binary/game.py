"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random
import map_generator

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"
SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

def handle_left(self, press):
    if(press):
        self.player.change_x = -2
    else:
        self.player.change_x = 0
def handle_right(self, press):
    if(press):
        self.player.change_x = 2
    else:
        self.player.change_x = 0
def handle_up(self, press):
    if(press):
        self.player.change_y = 2
    else:
        self.player.change_y = 0
def handle_down(self, press):
    if(press):
        self.player.change_y = -2
    else:
        self.player.change_y = 0
def handle_space(self, press):
    self.root = map_generator.Room(map_generator.ROOM_W, 
                                map_generator.ROOM_H, 
                                (random.randrange(0,255), 
                                random.randrange(0,255), 
                                random.randrange(0,255)), 
                                [None]*map_generator.MAX_ROOM_NEIGH, 
                                (0,0))
                    
    map_generator.generate([self.root], 0, 0)

class MyGame(arcade.Window):

    key_mapping = {
        arcade.key.A: handle_left,
        arcade.key.D: handle_right,
        arcade.key.W: handle_up,
        arcade.key.S: handle_down,
        arcade.key.SPACE: handle_space
    }
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.csscolor.WHITE_SMOKE)
        self.root = None
        self.player = None
        self.RoomList = None
        self.player_list = None
        self.physics_engine = None
        self.room = None
        self.current_room = None
        self.wall = None
        self.wall_list = None
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here
        self.player = arcade.SpriteSolidColor(40, 40, arcade.csscolor.BLACK)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.wall_list = arcade.SpriteList()

        for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
            for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
                self.wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                self.wall.left = x
                self.wall.bottom = y
                self.wall_list.append(self.wall)

    # Create left and right column of boxes
        for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
            for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
                # Skip making a block 4 and 5 blocks up
                if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5) or x != 0:
                    self.wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
                    self.wall.left = x
                    self.wall.bottom = y
                    self.wall_list.append(self.wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    def on_draw(self):
        arcade.start_render()
        """
        Render the screen.
        """
        
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame

        # Call draw() on all your sprite lists below

        self.draw_rooms([self.root], 0, (-1,0))
        self.player_list.draw()
        self.wall_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.physics_engine.update()

    def on_key_press(self, key, key_modifiers):
        if key in self.key_mapping:
            self.key_mapping[key](self, True)
        else:
            pass


    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key in self.key_mapping:
            self.key_mapping[key](self, False)
        else:
            pass

    def draw_rooms(self, rooms, count, idx):
        if(count == map_generator.MAX_ROOM_NUM): 
            return
        else:
            for room in rooms:
                for neighbor in room.neighbors:
                    if (neighbor is not None and room.id == idx):
                        arcade.draw_rectangle_filled(neighbor.x, neighbor.y, roneighborom.width, neighbor.height, neighbor.color)
                        return
                    else:
                        count+=1
                        self.draw_rooms([neighbor], count, neighbor.id)


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()