import arcade


class Base:
    display: arcade.Window

    spritelist: arcade.SpriteList
    spritedict: dict

    sceneTime: float = 0

    def update(self, delta_time: float) -> None:
        self.sceneTime += delta_time

    def draw(self) -> None:
        pass

    def reset(self) -> None:
        self.sceneTime = 0

    def mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        pass

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def key_press(self, key, modifiers):
        pass
