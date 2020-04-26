# Trio Survivals

## Authors: Pixel Soup ([Franccisco](https://github.com/Franccisco), [davidoluwafemi](https://github.com/davidoluwafemi))

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Navigation
1. Description
2. Installation
3. Running the game
4. Usage
5. Sources
6. License

### Description
One apocalypse, three different dimensions... wait, Three apocalypses then?

Call it how you like. Time is running, save yourself before it's too late!

This is a Parallel Escape game, where you and two more people will be playing together, but in different dimensions. That said, the outcome of the dimension you are will depend on your decisions.

### Installation
1. Install pipenv. It can be installed via pip:

```
pip install --user pipenv
```

*With `--user`, pipenv will be installed locally*.

Problems installing `pipenv`? Check the [installation instructions](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) in the pipenv documentation.

2. Clone this repository using `git clone https://github.com/python-discord/game-jam-2020.git`

3. Open the `game-jam-2020` folder and navigate into the `Pixel Soup` directory.

4. Inside `Pixel Soup`, open a terminal and run

```
pipenv install
```

### Running the game
Now that you installed the game, it's time to use it! In  the Pixel Soup directory, open a terminal (or use the one you opened when installed the game) and run

```
pipenv run start
```

**Important:** given the way that the `start` command works (loading the `main.py` file as a module), you **must** use it inside the Pixel Soup directory, otherwise the game will crash at startup.

### Usage
Once you open the game, press the S and you'll be moved into a waiting room. If you're the first player joining, you'll be the host. The game will start automatically when three players are in the room.


#### Key bindings

| Key                | Action            |
| ------------------ | ----------------- |
| **W** or **Space** | Jump              |
| **A** or **←**     | Move to the left  |
| **D** or **→**     | Move to the right |

### Sources

### License
This game is licensed by the MIT License. The details are located at `Pixel Soup/LICENSE`.
