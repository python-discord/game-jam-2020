import arcade


class Sprite(arcade.Sprite):
    @classmethod
    def from_texture(cls, texture: arcade.Texture, *args, **kwargs) -> arcade.Sprite:
        self = cls(*args, **kwargs)
        self.texture = texture
        return self
