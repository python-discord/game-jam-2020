# Monkeys & Frogs on Fire

## Triple Vision
"Triple Vision" is a dungeon 2d game.
[TODO]



## Game Implementation
The player has 3 different wizards to pick from: red, green, or blue. Each colored wizard has their own special abilities.

| Color | Description | Attack Multiplier (/\\) | Speed Multiplier (/\\) | Resistance (/\\) | Dexterity (\\/) | Special Ability |
| :-: | :-- | :-: | :-: | :-: | :-: | :-- |
| Red   | Strong and powerful, destroying all who dare defy him. | 1.5 | 1.1 | 0.1 | 0.6 | A floor smash, killing everything within a 5 block radius.
| Green | Built like a tank and as strong as a brick, this wizard can take a punch. | 1.1 | 1 | 0.5 | 0.75 | Invincibility and regeneration for 8 seconds (40hp/sec).
| Blue | Quick and fast, speeding through enemy ranks. | 1 | 1.5 | 0 | 0.5 | Flash time - Moving so fast that everything else appears slow.

*Note: ( /\ ) means a higher value is better and ( \\/ ) means a lower value is better*

When hovering over a card to select a specific colored wizard, the game slows down time, making everything move in slow motion.

The player can move around the map by clicking on a tile. The wizard will then use A* pathfinding to figure out its way over to the player's selected destination.

The map is generated using cellular automata through several generations. The map consists of three things, The flooring, walls, and spikes. The spikes periodically extend up out of the ground, and if the player is on top of them, they will be damaged.

The player and some specific enemies are able to shoot laser projectiles at each other, causing damage to the one entity hit. Currently, we have two enemies: The chasing demons and stationary imps. The chasing demons will chase the player if within range, and use melee attacks. On the other hand, stationary imps will *not* chase the player. Instead, they will sit still and fire lasers when the player is within range.

I think that's about it for our current game implementation.



### Game Peeks
[TODO]
