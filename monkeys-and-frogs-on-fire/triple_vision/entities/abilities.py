import enum

from triple_vision.entities.weapons import FloorStompMelee
from triple_vision.sound import SoundManager

# Abilities without duration need to use this
# This will make player unable to change character for 1s
INSTANT_DURATION = 1


class BaseAbility:
    base_cool_down = 30.0

    def __init__(self, duration: int, activate_sound: str = None, deactivate_sound: str = None):
        if duration >= self.base_cool_down:
            raise Exception("Ability duration cannot be higher than base cool-down.")
        self.duration = duration
        self.activate_sound = activate_sound
        self.deactivate_sound = deactivate_sound
        SoundManager.add_sound(activate_sound)
        SoundManager.add_sound(deactivate_sound)

    def activate(self, x, y, view_reference):
        """To be overwritten"""
        print("Ability activation not yet implemented")

    def deactivate(self, view_reference):
        """To be overwritten (if the ability can be deactivated)"""
        pass


class TimeSlow(BaseAbility):
    DURATION = 10

    def __init__(self, **kwargs):
        super().__init__(self.DURATION, **kwargs)

    def activate(self, x, y, game_view_reference):
        game_view_reference.time_slow_ability = True
        SoundManager.play_sound(self.activate_sound)

    def deactivate(self, game_view_reference):
        game_view_reference.time_slow_ability = False
        SoundManager.play_sound(self.deactivate_sound)


class FloorStomp(BaseAbility):
    def __init__(self, **kwargs):
        super().__init__(duration=INSTANT_DURATION, **kwargs)

    def activate(self, x, y, view_reference):
        floor_stomp = FloorStompMelee(
            center_x=view_reference.player.center_x,
            center_y=view_reference.player.center_y,
        )
        view_reference.game_manager.player_melee_attacks.append(floor_stomp)
        view_reference.game_manager.effects.append(floor_stomp.effect_sprite)
        SoundManager.play_sound(self.activate_sound)


class Indestructible(BaseAbility):
    DURATION = 8

    def __init__(self, **kwargs):
        super().__init__(self.DURATION, **kwargs)

    def activate(self, x, y, game_view_reference):
        game_view_reference.player.resistance = 1.0
        game_view_reference.player.regenerating_hp = True
        game_view_reference.player.regeneration_hp_value = 40
        game_view_reference.player.color = (255, 255, 255, 100)
        SoundManager.play_sound(self.activate_sound)

    def deactivate(self, game_view_reference):
        game_view_reference.player.reset_stats()
        game_view_reference.player.regenerating_hp = False
        game_view_reference.player.regeneration_hp_value = game_view_reference.player.DEFAULT_HP_REGENERATION_PER_S
        game_view_reference.player.color = (255, 255, 255, 255)
        SoundManager.play_sound(self.deactivate_sound)


class Abilities(enum.Enum):
    # Key are names, values are subclass of BaseAbility
    blue = TimeSlow(
        activate_sound="powerup_3.wav",
        deactivate_sound="powerup_4.wav"
    )
    red = FloorStomp(
        activate_sound="powerup_3.wav",
        deactivate_sound="powerup_4.wav"
    )
    green = Indestructible(
        activate_sound="powerup_3.wav",
        deactivate_sound="powerup_4.wav"
    )
