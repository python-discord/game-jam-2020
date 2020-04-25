import enum


from triple_vision.entities.weapons import FloorStompMelee


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
        pass


class TimeSlow(BaseAbility):
    DURATION = 10

    def __init__(self):
        super().__init__(self.DURATION)

    def activate(self, x, y, game_view_reference):
        game_view_reference.time_slow_ability = True

    def deactivate(self, game_view_reference):
        game_view_reference.time_slow_ability = False


class FloorStomp(BaseAbility):
    def __init__(self):
        # Instant ability no duration
        super().__init__(duration=0)

    def activate(self, x, y, view_reference):
        floor_stomp = FloorStompMelee(
            center_x=view_reference.player.center_x,
            center_y=view_reference.player.center_y,
        )
        view_reference.game_manager.player_melee_attacks.append(floor_stomp)
        view_reference.game_manager.effects.append(floor_stomp.effect_sprite)


class Indestructible(BaseAbility):
    DURATION = 5

    def __init__(self):
        super().__init__(self.DURATION)


class Abilities(enum.Enum):
    # Key are names, values are subclass of BaseAbility
    blue = TimeSlow()
    red = FloorStomp()
    green = Indestructible()
