#Indecisive

This is team Indecisive's submission to the Python Discord's Game Jam.

This Game Jam have the theme `Three of a kind` with the addition requirements of:
 - Your project must use the Python Arcade Library. 
 It is not permitted to work around this by, e.g., using the Python Arcade Libary as a wrapper for another framework.
 - The majority of your project must be written in Python.
 - Your project must be feasible to run and simple to set up on a desktop computer.
 - You are allowed to use existing assets, like images and sound effects, as long as the licenses of those assets permit it. 
 Typically, this means that the assets are licensed under an OSI-approved or Creative Commons license, or is in the public domain.
 - All projects should start from scratch and all code must be written within the time constrictions of the jam.


To Play the Game:
    - There must be a host that run the Play as host section:
        - The host must open the TCP port 1000 in order for the game to work.
    - The other two players connect to the game via the Play as a client menu.
    - In order for the client to connect to the server the ip address must be entered in the black box on the screen.
    - Then all players must enter a name in the black box of the next screen.
    - Then the host can start the game by pressing "Start".
    
Using Python 3.8
 
`python -m venv venv`

activate virtual environment

`pip install arcade websocket`

`python -m game`
