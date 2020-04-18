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

class MyGame(arcade.Window):
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

        self.RoomList = None

        self.rooms = None
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here
        self.RoomList = arcade.SpriteList

    def on_draw(self):
        arcade.start_render()
        """
        Render the screen.
        """
        
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame

        # Call draw() on all your sprite lists below
        for x in range(0, SCREEN_WIDTH, map_generator.ROOM_W):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.csscolor.BLACK)
        for y in range(0, SCREEN_HEIGHT, map_generator.ROOM_H):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, arcade.csscolor.BLACK)

        self.draw_rooms(self.rooms)
                

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        if(key == arcade.key.SPACE):
            self.root = map_generator.Room(map_generator.ROOM_W, map_generator.ROOM_H, (random.randrange(0,255), 
                            random.randrange(0,255), 
                            random.randrange(0,255)), 
                            [None]*map_generator.MAX_ROOM_NEIGH, "root", 
                            SCREEN_WIDTH // 2, 
                            SCREEN_HEIGHT // 2)
                        
            self.rooms = map_generator.generate([self.root])

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def draw_rooms(self, rooms):
        if(rooms is not None):
            for room in rooms:
                if(room is not None):
                    arcade.draw_rectangle_filled(room.x, room.y, room.width, room.height, room.color)
                    for neighbor in room.neighbors:
                        if (neighbor is not None):
                            arcade.draw_rectangle_filled(neighbor.x, neighbor.y, neighbor.width, neighbor.height, neighbor.color)



def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()