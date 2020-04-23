import arcade


class Sound(arcade.Sound):
    def __init__(
        self, *args, is_faded: bool = False, max_volume: float = 1.0, **kwargs
    ) -> None:
        self.faded = is_faded
        self.max_volume = max_volume
        super().__init__(*args, **kwargs)

    def set_volume(self, volume):
        if volume > self.max_volume:
            return
        super().set_volume(volume)
