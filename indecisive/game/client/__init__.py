
print("0-network, 1-game")

x = int(input())

if x == 0:
    from . import network
else:
    from . import graphics
    graphics.main()