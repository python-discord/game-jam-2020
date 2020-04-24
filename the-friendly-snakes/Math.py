class Maths:
    @classmethod
    def lerp(cls, v1: float, v2: float, u: float):
        return v1 + ((v2 - v1) * u)

    @classmethod
    def clamp(cls, x: float, lowerlimit: float, upperlimit: float):
        if x < lowerlimit:
            x = lowerlimit
        if x > upperlimit:
            x = upperlimit
        return x

    @classmethod
    def smoothstep(cls, edge0: float, edge1: float, x: float):
        x = Maths.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return x * x * x * (x * (x * 6 - 15) + 10)

    @classmethod
    def lowlimit(cls, x, lowerlimit):
        if x < lowerlimit:
            x = lowerlimit
        return x

    @classmethod
    def maxlimit(cls, x, upperlimit):
        if x > upperlimit:
            x = upperlimit
        return x