
def lerp(a, b, amount):
    return (amount * a) + ((1 - amount) * b)

def smoothstep(edge0, edge1, amount):
    x = clamp((amount - edge0) / (edge1 - edge0), 0.0, 1.0)
    
    return x * x * (3 - 2 * x)

def smootherstep(edge0, edge1, amount):
    x = clamp((amount - edge0) / (edge1 - edge0), 0.0, 1.0)

    return x * x * x * (x * (x * 6 - 15) + 10)

def smoothererstep(edge0, edge1, amount):
    x = clamp(amount, 0.0, 1.0)

    return x^5

def clamp(x, lower_limit, upper_limit):
    if (x < lower_limit):
        x = lower_limit
    if (x > upper_limit):
        x = upper_limit
    return x

def create_hit_box(width, height):
    w2 = width / 2
    h2 = height / 2

    return [
        [-w2, -h2],
        [-w2, h2],
        [w2, h2],
        [w2, -h2]
    ]