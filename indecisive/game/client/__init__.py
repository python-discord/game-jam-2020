
print("0-network, 1-game")

x = 1

if x == 0:
    from . import network
else:
    from . import graphics
    graphics.main()