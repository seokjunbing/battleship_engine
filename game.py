from player import *

# CONSTANTS
DEFAULT = 0  # represents cells that have not been shot
MISS = 1  # represents cells that have missed shots
HIT = 2  # represents cells that are occupied and have been shot
SUNK = 3  # represents cells with sunken ships
OCCUPIED = 4  # represents cells containing ships that have not been hit


class Game(object):
    def __init__(self, p1_name, p2_name, board_size=(10, 10)):
        """
        Initializer for Game class
        :param p1_name: player1's name (string)
        :param p2_name: player2's name (string)
        :param board_size: default size is 10 by 10 (2-tuple)
        """
        self.player1 = Player(p1_name, board_size)
        self.player2 = Player(p2_name, board_size)
        self.board_x = board_size[0]
        self.board_y = board_size[1]
        self.turn = 0
        self.game_over = False

        # Current default ships, can be expanded by .add_custom_ship() method
        self.ships = [("Carrier", (1, 5)),
                      ("Battleship", (1, 4)),
                      ("Submarine", (1, 3)),
                      ("Cruiser", (1, 2)),
                      ("Destroyer", (1, 2))]

    def add_custom_ship(self, ship_name, dimensions):
        """
        Method to add custom sized ships to the game. This is an optional method that is not necessary to play the game.
        :param ship_name: name of the custom ship (string)
        :param dimensions: dimensions of the custom ship (2-tuple). The order of 2-tuple does not matter.
            E.g. (2,3) and (3,2) are the same.
        :return: does not return
        """
        self.ships.append((ship_name, dimensions))

    def initialize_ships(self, p1_pos_or, p2_pos_or):
        """
        Method to initialize player1 and player2 ships
        :param p1_pos_or: a list of 2-tuple containing coords and orientation of player1's ships. Each tuple is a form
            of ((x, y), orientation). (x, y) is a pair of integers representing the location of the TOP LEFT-MOST cell
            of a ship's desired location. orientation is the direction to place the ship. orientation can either be
            'vertical' (longest dimension of ship along the y-axis) or ''horizontal' (longest dimension of ship along
            the x-axis)
        :param p2_pos_or: same as p1_pos_or but for player2
        :return: does not return
        """
        if len(p1_pos_or) != len(self.ships):
            raise ValueError("length of p1_pos_or and self.ships must match")
        if len(p2_pos_or) != len(self.ships):
            raise ValueError("length of p2_pos_or and self.ships must match")

        for i in range(0, len(self.ships)):
            self.player1.place_ship(self.ships[i][0], p1_pos_or[i][1], self.ships[i][1], p1_pos_or[i][0])
            self.player2.place_ship(self.ships[i][0], p2_pos_or[i][1], self.ships[i][1], p2_pos_or[i][0])

    def take_turn(self, coord_to_shoot):
        """
        Method that actually 'plays' the game. This method automatically decides whose turn it is to place a shot.
            Thus, it only requires target coordinate as its function parameter. After every shot, this method checks if
            the game is over.
        :param coord_to_shoot: target coordinate to shoot. (2-tuple of integers)
        :return: does not return
        """
        if self.turn % 2 == 0:
            attacker = self.player1
            receiver = self.player2
        else:
            attacker = self.player2
            receiver = self.player1

        print("\n%s's turn:" % attacker.name)

        attacker.shoot_and_update_boards(receiver, coord_to_shoot)

        self.turn += 1

        if receiver.is_dead():
            print("\nGame Over: %s wins, %s loses\n" % (attacker.name, receiver.name))
            self.game_over = True

    def is_game_over(self):
        return self.game_over

    def get_player1_boards(self):
        """
        method to simply return two boards states of player1
        :return: (b1, b1) where b1 is a list of lists containing the current state of the player1's tracking board
            and b2 is a list of lists containing the current state of the board containing player1's own ships
        """
        return self.player1.get_tracking_board_as_list(), self.player1.get_my_ships_as_list()

    def get_player2_boards(self):
        """
        method to simply return two boards states of player2
        :return: (b1, b1) where b1 is a list of lists containing the current state of the player2's tracking board
            and b2 is a list of lists containing the current state of the board containing player2's own ships
        """
        return self.player2.get_tracking_board_as_list(), self.player2.get_my_ships_as_list()

    def pretty_print_player1_boards(self):
        """
        print ascii representation of player1's boards
        :return: does not return
        """
        self.player1.pretty_print_tracking_board()
        self.player1.pretty_print_my_ships()

    def pretty_print_player2_boards(self):
        """
        print ascii representation of player2's boards
        :return: does not return
        """
        self.player2.pretty_print_tracking_board()
        self.player2.pretty_print_my_ships()


# Below is a simple demonstration / test to highlight the usage of functions above.
# The flow should be:
#       initialize a game object -> (optional) add custom ships -> initialize ships -> (repeat) take_turn()
if __name__ == "__main__":
    board_size = (10, 10)
    g = Game("John", "Sam", board_size)
    g.add_custom_ship("custom1", (2, 2))
    g.add_custom_ship("custom2", (1, 1))

    p1_positions_orientations = [((0, 0), 'horizontal'),
                                 ((0, 1), 'vertical'),
                                 ((2, 3), 'horizontal'),
                                 ((6, 5), 'vertical'),
                                 ((4, 8), 'horizontal'),
                                 ((8, 0), 'horizontal'),
                                 ((9, 9), 'vertical')]

    p2_positions_orientations = [((0, 0), 'vertical'),
                                 ((3, 0), 'horizontal'),
                                 ((7, 4), 'horizontal'),
                                 ((2, 8), 'vertical'),
                                 ((7, 1), 'vertical'),
                                 ((3, 8), 'vertical'),
                                 ((0, 9), 'horizontal')]

    g.initialize_ships(p1_positions_orientations, p2_positions_orientations)

    g.pretty_print_player1_boards()
    g.pretty_print_player2_boards()

    test_movements = [((0, 0), (0, 4)),
                      ((0, 1), (0, 5)),
                      ((0, 2), (0, 3)),
                      ((0, 3), (0, 2)),
                      ((0, 4), (0, 1)),
                      ((0, 9), (0, 0)),
                      ((1, 6), (1, 6)),
                      ((3, 0), (1, 7)),
                      ((4, 0), (3, 2)),
                      ((5, 0), (3, 3)),
                      ((2, 0), (2, 3)),
                      ((6, 0), (4, 3)),
                      ((2, 7), (1, 2)),
                      ((2, 8), (8, 0)),
                      ((2, 9), (7, 0)),
                      ((3, 8), (6, 0)),
                      ((3, 9), (1, 9)),
                      ((4, 8), (2, 9)),
                      ((4, 9), (3, 9)),
                      ((9, 0), (4, 9)),
                      ((7, 2), (6, 5)),
                      ((7, 1), (6, 6)),
                      ((7, 6), (8, 1)),
                      ((9, 3), (8, 2)),
                      ((7, 4), (9, 0)),
                      ((8, 4), (9, 1)),
                      ((9, 4), (5, 5))]

    for entry in test_movements:
        for t in entry:
            g.take_turn(t)
            if g.is_game_over():
                break

    g.pretty_print_player1_boards()
    g.pretty_print_player2_boards()

    p1b1, p1b2 = g.get_player1_boards()
    p2b1, p2b2 = g.get_player2_boards()
