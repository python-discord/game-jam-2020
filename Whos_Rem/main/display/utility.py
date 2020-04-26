from functools import reduce
import arcade


class ListFunctions:

    @classmethod
    def dot_sum(cls, *iterables):
        sums = map(cls.add, *iterables)

        return list(sums)

    @classmethod
    def dot_average(cls, *iterables):
        num_of_lists = len(iterables)
        sums = cls.dot_sum(*iterables)
        average = map(cls.div, sums, cls.repeat(num_of_lists))

        return list(average)

    @classmethod
    def dot_product(cls, *iterables):
        products = map(cls.product, *iterables)

        return list(products)

    @staticmethod
    def multiply_list(iterable, value):
        return [num * value for num in iterable]

    @staticmethod
    def add(*nums):
        return sum(nums)

    @staticmethod
    def div(number, divisor):
        return number / divisor

    @staticmethod
    def product(*nums):
        return reduce(lambda x, y: x * y, nums)

    @staticmethod
    def int_list(iterable):
        return [int(num) for num in iterable]

    @staticmethod
    def repeat(number):
        while True:
            yield number


class ColourBlend:

    @staticmethod
    def brightness(colour, brightness, as_int=True):
        new_colour = [col*brightness for col in colour]
        if as_int:
            new_colour = ListFunctions.int_list(new_colour)

        return new_colour

    @staticmethod
    def colour_fade(first_colour, second_colour, number_of_steps, as_int=True):
        colours = []
        for step in range(number_of_steps):
            colour_1 = ListFunctions.multiply_list(first_colour, 1 - step/number_of_steps - 1)
            colour_2 = ListFunctions.multiply_list(second_colour, step/(number_of_steps - 1))
            merged_colour = (ListFunctions.dot_sum(colour_1, colour_2))
            if as_int:
                merged_colour = ListFunctions.int_list(merged_colour)
            colours.append(merged_colour)

        return colours

    @staticmethod
    def brightness_cycle(brightness=1, step=0.02):
        mult = -1
        while True:
            yield brightness

            if brightness == 1:
                mult = -1
            elif brightness == 0:
                mult = 1
            brightness += step * mult

    @staticmethod
    def rainbow_cycle(step=16):
        colour = [255, 0, 0]
        while True:
            yield colour
            if colour[0] == 255 and colour[1] < 255 and colour[2] == 0:
                colour[1] += step
            elif colour[1] == 255 and colour[0] > 0 and colour[2] == 0:
                colour[0] -= step
            elif colour[1] == 255 and colour[2] < 255 and colour[0] == 0:
                colour[2] += step
            elif colour[2] == 255 and colour[1] > 0 and colour[0] == 0:
                colour[1] -= step
            elif colour[2] == 255 and colour[0] < 255 and colour[1] == 0:
                colour[0] += step
            elif colour[0] == 255 and colour[2] > 0 and colour[1] == 0:
                colour[2] -= step

            for index in range(len(colour)):
                colour[index] = min(colour[index], 255)
                colour[index] = max(colour[index], 0)

