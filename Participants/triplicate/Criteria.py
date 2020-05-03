
class Criteria:
    def __init__(self):
        pass

    def check(self, other):
        pass


class AndCriteria(Criteria):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def check(self, other):
        return self.first.check(other) and self.second.check(other)


class OrCriteria(Criteria):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def check(self, other):
        return self.first.check(other) or self.second.check(other)


class IsTypeCriteria(Criteria):
    def __init__(self, types):
        self.types = types

    def check(self, other):
        if other.type in self.types:
            return True
        return False


class IsNotTypeCriteria(Criteria):
    def __init__(self, types):
        self.types = types

    def check(self, other):
        if other.type in self.types:
            return False
        return True


class IsFormCriteria(IsTypeCriteria):
    def __init__(self):
        super().__init__(["Form"])


class IsNotFormCriteria(IsNotTypeCriteria):
    def __init__(self):
        super().__init__(["Form"])


class IsColorCriteria(Criteria):
    def __init__(self, color):
        self.color = color

    def check(self, other):
        # print("Self: {} Other: {}".format(self.color,other.color))
        if other.color == self.color:
            return True
        return False


class IsColorInCriteria(Criteria):
    def __init__(self, colors):
        self.colors = colors

    def check(self, other):
        # print("Self: {} Other: {}".format(self.color,other.color))
        if other.color in self.colors:
            return True
        return False


class IsNotColorCriteria(Criteria):
    def __init__(self, color):
        self.color = color

    def check(self, other):
        if other.color == self.color:
            return False
        return True


class IsColorNotInCriteria(Criteria):
    def __init__(self, colors):
        self.colors = colors

    def check(self, other):
        # print("Self: {} Other: {}".format(self.color,other.color))
        if other.color not in self.colors:
            return True
        return False


class EvenNumberCriteria(Criteria):
    def check(self, other):
        if other.val % 2 == 0:
            return True
        return False


class OddNumberCriteria(Criteria):
    def check(self, other):
        if other.val % 2 == 1:
            return True
        return False


class ExactValueCriteria(Criteria):
    def __init__(self, val):
        self.val = val

    def check(self, other):
        if other.val == self.val:
            return True
        return False