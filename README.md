# Battleship Game Engine
by SeokJun Bing (aka Jun)

Coded in python2.7 environment

## Files
`./game.py` contains the Game class which is the engine of the game that initializes Player and Ship classes.
 Contains an example that does a basic test run of the game and highlights usage.<br>
`./player.py`contains the Player class. Responsible for the main bulk of game logic and rules.<br>
`./ship.py`contains the Ship class<br>

## Statisfies the following requirements
* Allow to start a new 2-player game (i.e. each player places their pieces)

* Ability to return the board-states at any point in time (i.e. which cells are occupied/hit/sunk)<br>
    
    * `game.get_player1_boards()` and `game.get_player2_boards()` returns nested lists<br>
    * `game.pretty_print_player1_boards()` and `game.pretty_print_player2_boards()` prints ascii representation of the boards
    

* Allow players to take turns shooting at a 1x1 target cell<br>
    * `game.take_turn(coordinate)`
        * automatically decides whose turn it is and shoots at `coordinate`

* Ability to signal when a ship is sunk
    * Whenever a ship is sunk a message is printed to stdout.<br>
        * E.g. `Sam's Destroyer is sunk`

* Ability to signal when someone wins or loses
    * When all of a player's ships are sunk a message is printed to stdout.<br>
        * E.g. `Game Over: John wins, Sam loses`
    * `game.is_game_over()` returns a boolean indicating if the current game is finished
* Ability to play on a default 10 by 10 board with these default ships.
    * Carrier - 1x5
    * Battleship - 1x4
    * Submarine - 1x3
    * Cruiser - 1x2
    * Destroyer - 1x2
* Extensibility
    * Able to use board sizes other than 10 by 10
        * Board size is an input to the Game class initializer
        * Can also use non-square board sizes such as 10 by 15
    * Able to use custom ships such as a 2x2 Petrol piece and/or multiple pieces
        * `game.add_custom_ship()` allows addition of new ships of any size
    