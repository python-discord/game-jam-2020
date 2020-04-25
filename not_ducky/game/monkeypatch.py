import arcade


class SpriteList(arcade.SpriteList):
    def draw(self):
        for item in self.sprite_list:
            item.draw()
            # item.draw_hit_box(arcade.color.WHITE)
