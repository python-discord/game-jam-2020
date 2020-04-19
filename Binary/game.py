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

def handle_left(self, press):
    if(press):
        self.player.change_x = -5
    else:
        self.player.change_x = 0
def handle_right(self, press):
    if(press):
        self.player.change_x = 5
    else:
        self.player.change_x = 0
def handle_up(self, press):
    if(press):
        self.player.change_y = 5
    else:
        self.player.change_y = 0
def handle_down(self, press):
    if(press):
        self.player.change_y = -5
    else:
        self.player.change_y = 0

class MyGame(arcade.Window):

    key_mapping = {
        arcade.key.A: handle_left,
        arcade.key.D: handle_right,
        arcade.key.W: handle_up,
        arcade.key.S: handle_down,
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
        self.current_room = None
        self.wall = None
        self.wall_list = None
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here
        self.root = map_generator.Room(map_generator.ROOM_W, 
                                map_generator.ROOM_H, 
                                (random.randrange(0,255), 
                                random.randrange(0,255), 
                                random.randrange(0,255)), 
                                [None]*map_generator.MAX_ROOM_NEIGH, 
                                (0,0),
                                None)
                    
        map_generator.generate([self.root], 0, 0)

        self.player = arcade.SpriteSolidColor(40, 40, arcade.csscolor.BLACK)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.wall_list = arcade.SpriteList()
        self.current_room = self.root

        for y in (0, SCREEN_HEIGHT):
        # Loop for each box going across
            for x in range(0, SCREEN_WIDTH):
                self.wall = arcade.SpriteSolidColor(1,0,arcade.csscolor.WHITE)
                self.wall.left = x
                self.wall.bottom = y
                self.wall_list.append(self.wall)

    # Create left and right column of boxes
        for x in (0, SCREEN_WIDTH):
        # Loop for each box going across
            for y in range(0, SCREEN_WIDTH):
                self.wall = arcade.SpriteSolidColor(1,0,arcade.csscolor.WHITE)
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

        self.draw_room_with_neighbors(self.current_room)
        self.player_list.draw()
        #self.draw_room_smol([self.root], 1)
        self.wall_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.physics_engine.update()
        self.update_player_room()
        self.set_viewport(self.player.center_x - SCREEN_WIDTH / 2, self.player.center_x + SCREEN_WIDTH / 2, self.player.center_y - SCREEN_HEIGHT / 2, self.player.center_y + SCREEN_HEIGHT / 2)

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

    def draw_room_with_neighbors(self, room):
        self.draw_room(room)
        for n in self.root.neighbors:
            if n is not None:
                self.draw_room(n)
 
    def draw_room(self, room):
        x, y = room.id
        width, height = room.width, room.height
        arcade.draw_rectangle_filled(x * width + width / 2, y * height + height / 2, width, height, room.color)
 
    def update_player_room(self):
        player_x = self.player.center_x
        player_y = self.player.center_y
 
        node_ix, node_iy = self.current_room.id
        node_width = self.current_room.width
        node_height = self.current_room.height
 
        node_x = node_ix * node_width
        node_y = node_iy * node_height
 
        if player_x > node_x + node_width:
            # go right
            next_id = node_ix + 1, node_iy
        elif player_x < node_x:
            # go left
            next_id = node_ix - 1, node_iy
        elif player_y > node_y + node_height:
            # go up
            next_id = node_ix, node_iy + 1
        elif player_y < node_y:
            # go down
            next_id = node_ix, node_iy - 1
        else:
            return
 
        for n in self.current_room.neighbors:
            if n is not None and n.id == next_id:
                self.current_room = n
                break

"""    def draw_room_smol(self, rooms, count):
        if(count == map_generator.MAX_ROOM_NUM): 
            return
        else:
            for room in rooms:
                for neighbor in room.neighbors:
                    if neighbor is not None:
                        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2 + (20 * count) , SCREEN_HEIGHT // 2 + (20 * count) // 2, 20, 20,neighbor.color)
                        count+=1
                        self.draw_rooms([neighbor], count)"""


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()