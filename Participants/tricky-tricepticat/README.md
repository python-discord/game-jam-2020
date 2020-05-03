*Tricky Tricepticat - Python Discord Game Jam 2020*<br>
*(DomicidalManiac#5836)*
# Brawn, Brain, and Bald
*NOTE: This game is currently a very rough draft with not much gameplay.* <br>
A game about three pirates who sail the seas and fight monsters in island dungeons.
Ideally, there would be 3 islands with 1 boss per island. 
Right now there is just a basic sailing/naval combat system and a *very* basic dungeon combat system.

### Current Game Features
* Basic sailing mechanics
* Basic naval combat
* Ship damage
* Basic sword combat
* Custom TMX layer pathfinding functions

### Dependencies
* Python 3.7+
* [arcade](https://arcade.academy/index.html)
* pathfinding

## Download it
* `git clone https://github.com/DomicidalDesigns/game-jam-2020.git`

## Install it
* `cd` to `game-jam-2020/tricky-tricepticat/`
* `python -m pipenv install`<br>

**If you have multiple python versions, instead specify one using:**
* `python -m pipenv install --python 3.7` <br>where `3.7` is your python version, 3.7 or newer

## Run it
* `python -m pipenv run start`

## Play it
### Ship
`W` - Lower sails (accelerate) <br>
`S` - Raise sails (decelerate <br>
`A` - Turn CCW <br>
`D` - Turn CW <br>

`Q` - Fire port cannon <br>
`E` - Fire starboard cannon <br>

### Dungeon
`LEFT CLICK` - Attack <br>
`WSAD` - Movement <br>

### General
`F11` - Toggle FULLSCREEN
`=` - Zoom in
`-` - Zoom out

### Overview
You start out on the run from enemy ships. Your goal is to escape from them or destroy them and make it to the port at one of the islands. Once you make it to the port, you can enter the dungeon by pressing `SPACE`. Once you've defeated all the enemies here, you've won the game!

## Acknowledgments
Thank you to the creators of the assets used in this game.
If you liked any of their content, consider using them in your game and supporting their work.
* [kenney](https://www.kenney.nl/assets/) - Pirate Pack (tileset and ships)
* [Pixel Poem](https://pixel-poem.itch.io/dungeon-assetpuck) - Dungeon asset pack
* [Wenrexa](https://wenrexa.itch.io/) - Sword cursor
* [FinalGateStudios](https://finalgatestudios.itch.io/undead-sprite-pack) - undead sprites
* [KingKelpo](https://kingkelp.itch.io/sword) - sword sprite
* [WSSS](https://wellingtonseashantysociety.bandcamp.com/track/great-open-sea) - Wellington Sea Shanty Society - Great Open Sea
* [AugustSandberg](https://freesound.org/people/AugustSandberg/sounds/265553/) - Ship ambient audio
* [Pixel Frog](https://pixel-frog.itch.io/) - Amazing pirate sprites

## Future Work / TODO
In the future I want to refine the pathfinding for enemies and further improve the dungeon crawling mechanics, incorporating different fighting styles for the three pirates. Brain would use the sword, Brawn would use his fists, and Bald would use explosives.
The player would be able to freely switch between the players, and the other two pirate NPCs would follow the player.

