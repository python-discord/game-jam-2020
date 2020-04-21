import random

class PatternGenerator:

    def __init__(self, lanes: list):
        self.lanes = lanes

    def generate_pattern(self):
        rand = random.randint(0, 99)
        if 0 <= rand <= 11:
            return []
        elif rand <= 34:
            return self._generate_one()
        elif rand <= 54:
            return self._generate_consecutives(2)
        elif rand <= 69:
            return self._generate_consecutives(3)
        elif rand <= 84:
            return self._generate_simultaneous(2)
        else:
            return self._generate_simultaneous(3)


    def _generate_one(self):
        return [self.lanes[random.randint(0, 2)].generate_obstacle()]

    def _generate_consecutives(self, repeat: int)-> list:
        rand = random.randint(0, len(self.lanes) - 1)
        result = []
        for numbers in range(repeat):
            result.append(self.lanes[rand].generate_obstacle())
        return result

    def _generate_simultaneous(self, number: int)-> list:
        if number > len(self.lanes):
            raise ValueError("More simultanous object requested than lanes available")
        possibilities = list(range(len(self.lanes)))
        result = []
        for obstacle in range(number):
            result.append(self.lanes[
                              possibilities.pop(
                                  random.randint(0, len(possibilities)-1))].generate_obstacle())
        return result
