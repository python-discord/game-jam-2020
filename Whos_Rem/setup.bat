@ECHO OFF

CALL pipenv install -r requirements.txt
CALL pipenv run python main_game.py

PAUSE