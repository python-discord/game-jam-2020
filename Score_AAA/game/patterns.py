from random import randint


class PatternGenerator:
    def __init__(self, lanes: list):
        self.lanes = lanes

    def generate_pattern(self):
        rand = randint(0, 99)
        if 0 <= rand <= 11:
            return [[]]
        elif rand <= 34:
            return self._generate_one("../ressources/E_Obstacle.png")
        elif rand <= 54:
            return self._generate_consecutives(2, "../ressources/W_Obstacle.png")
        elif rand <= 69:
            return self._generate_consecutives(3, "../ressources/W_Obstacle.png")
        elif rand <= 84:
            return self._generate_simultaneous(2, "../ressources/Q_Obstacle.png")
        else:
            return self._generate_simultaneous(3, "../ressources/Q_Obstacle.png")

    def _generate_one(self, sprite_path):
        return [self.lanes[randint(0, 2)].generate_obstacle(sprite_path)]

    def _generate_consecutives(self, repeat: int, sprite_path) -> list:
        rand = randint(0, len(self.lanes) - 1)
        result = []
        for numbers in range(repeat):
            result.append([self.lanes[rand].generate_obstacle(sprite_path)])
        return result

    def _generate_simultaneous(self, number: int, sprite_path) -> list:
        if number > len(self.lanes):
            raise ValueError("More simultanous object requested than lanes available")
        possibilities = list(range(len(self.lanes)))
        result = []
        for obstacle in range(number):
            result.append(
                self.lanes[
                    possibilities.pop(randint(0, len(possibilities) - 1))
                ].generate_obstacle(sprite_path)
            )
        return result
