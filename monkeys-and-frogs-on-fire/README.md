# Monkeys & Frogs on Fire

## Triple Vision
"Triple Vision" is a dungeon 2d game based on the theme "3 of a kind".



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

The player and some specific enemies are able to shoot laser projectiles at each other, causing damage to the entity hit. There are two types of enemies: The chasing, melee enemies and stationary, sharp shooters. The chasing enemies will chase the player if within range, and use melee attacks. On the other hand, stationary imps will *not* chase the player. Instead, they will sit still and fire lasers when the player is within range.



## Play the game!
- Run `pipenv sync`
- Start the server: `pipenv run server`
- Start the game: `pipenv run start`

You can play on the same server as your friends if you'd like and share leaderboards!

### Movement
- Your player moves with the WASD keys.

### Attacking
- Your player will fire a spell when you click on the left mouse button, the spell will move to the direction your cursor will point on while clicking. hold the left mouse button to shoot a charging spell which causes more damage and knockback!
- Your player will activate his powerup / ability when you press the right mouse button.

- Your mana bar will control your abilities and charged spells, if the mana bar is empty, you are helpless until its recharged.


### Entities
- You and all moving sprites can walk on the floor.
- You can pickup potions to increase your stats and the chance of you defeating the enemies.

### Characters
- To switch to a different character, simply hover on the card menu in the button right and click on the character you want to switch to, be aware that you cannot switch characters while using your powerup.

### Game ending
Kill all enemies in order to win and climb up levels, once all your hearts are empty, you die.

### Multiplayer??
Get the highest score and compete with your friends!

### Game Peeks
<img src="https://cdn.discordapp.com/attachments/693177507683369010/704005792197640232/unknown.png">
<img src="https://cdn.discordapp.com/attachments/693177507683369010/704006014554472498/unknown.png">
<img src="https://cdn.discordapp.com/attachments/693177507683369010/704016339895058443/unknown.png">
