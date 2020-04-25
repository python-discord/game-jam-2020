class BaseAbility:
    base_cool_down = 30.0

    def __init__(self, duration: int):
        if duration >= self.base_cool_down:
            raise Exception("Ability duration cannot be higher than base cool-down.")
        self.duration = duration

    def activate(self, x, y, view_reference):
        """To be overwritten"""
        print("Ability activation not yet implemented")

    def deactivate(self, view_reference):
        """To be overwritten (if the ability can be deactivated)"""
        print("Ability deactivation not yet implemented")


class TimeSlow(BaseAbility):
    DURATION = 10

    def __init__(self):
        super().__init__(self.DURATION)

    def activate(self, x, y, game_view_reference):
        game_view_reference.time_slow_ability = True

    def deactivate(self, game_view_reference):
        game_view_reference.time_slow_ability = False


class FloorStomp(BaseAbility):
    DURATION = 5

    def __init__(self):
        super().__init__(self.DURATION)


class Indestructible(BaseAbility):
    DURATION = 5

    def __init__(self):
        super().__init__(self.DURATION)
