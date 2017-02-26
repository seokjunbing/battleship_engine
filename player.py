from game import DEFAULT, MISS, HIT, SUNK, OCCUPIED
from ship import *


class Player(object):
    def __init__(self, player_name, board_dimension):
        self.name = player_name  # player name
        self.my_board = dict()  # keep track of the state of my fleet and missed shots on my territory
        self.tracking_board = dict()  # keep track of my shots on enemy territory
        self.board_x = board_dimension[0]
        self.board_y = board_dimension[1]
        self.life = 0  # life == 0 means that the player is dead

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def is_dead(self):
        if self.life == 0:
            return True
        return False

    def is_hit(self, coordinate):
        if coordinate in self.my_board.keys():
            if self.my_board[coordinate][1] == OCCUPIED:
                return True
        return False

    def _valid_shot(self, coordinate):
        """
        Check if a shot at a input coord is a valid shot, raise exceptions if not
        :param coordinate: (x,y) tuple of the coord to shoot
        :return: does not return
        """
        x, y = coordinate

        if x < 0 or y < 0:
            raise ValueError("Cannot shoot at a negative coordinate %s" % str(coordinate))
        elif x > self.board_x - 1 or y > self.board_y - 1:
            raise ValueError("Cannot shoot at a coordinate %s greater than the board size of %d by %d (zero indexed)" %
                             (str(coordinate), self.board_x, self.board_y))
        elif coordinate in self.tracking_board.keys():
            raise ValueError("Shot at %s had already been fired previously by %s" % (str(coordinate), self.name))

    def receive_damage(self, coordinate):
        """
        when hit, use this method to record the damage to the target ship and update the board the reflect being hit
        :param coordinate:
        :return:
        """
        self.my_board[coordinate][1] = HIT
        self.my_board[coordinate][0].receive_shot()
        self.life -= 1

    def shoot_and_update_boards(self, enemy, coordinate):
        """
        Shoot the enemy at the input coordinate and update the boards appropriately for both the shooter and the
            receiver
        :param enemy: enemy player to shoot
        :param coordinate: (x, y) tuple of where to shoot
        :return: does not return
        """
        self._valid_shot(coordinate)

        if enemy.is_hit(coordinate):
            self.tracking_board[coordinate] = HIT
            enemy.receive_damage(coordinate)

            print("%s hit %s's %s at %s" % (self.name, enemy.name, enemy.my_board[coordinate][0].name,
                                            str(coordinate)))

            if enemy.my_board[coordinate][0].is_sunk():
                print("%s's %s is sunk" % (enemy.name, enemy.my_board[coordinate][0].name))
                # update the boards as a ship has been sunk
                for c in enemy.my_board[coordinate][0].coordinates:
                    self.tracking_board[c] = SUNK
                    enemy.my_board[c][1] = SUNK
        else:
            print("%s's shot missed at %s" % (self.name, str(coordinate)))
            enemy.my_board[coordinate] = [None, MISS]
            self.tracking_board[coordinate] = MISS

    def _check_ship_overlap(self, ship_name, orientation, dimension, coordinate):
        """
        Helper method to check if the current placement of ship does not overlap with a pre-existing ship
        :param ship_name: name of the current ship being placed (string)
        :param orientation: 'vertical' (longest dimension of ship along the y-axis) or
            'horizontal' (longest dimension of ship along the x-axis)
        :param dimension: (m,n) tuple representing the dimensions of the input ship
        :param coordinate: TOP LEFT MOST coordinate of the ship is placed at this coordinate
        :return: does not return
        """

        d0, d1 = dimension
        x, y = coordinate

        longer_d = max(d0, d1)
        shorter_d = min(d0, d1)

        if orientation == 'vertical':
            for i in range(0, longer_d):
                for j in range(0, shorter_d):
                    if (x + j, y + i) in self.my_board:
                        raise ValueError("%s overlaps with %s at (%d,%d)" % (ship_name, self.my_board[(x + j, y + i)][0]
                                                                             , x + j, y + i))
        elif orientation == 'horizontal':
            for i in range(0, longer_d):
                for j in range(0, shorter_d):
                    if (x + i, y + j) in self.my_board:
                        raise ValueError("%s overlaps with %s at (%d,%d)" % (ship_name, self.my_board[(x + j, y + i)][0]
                                                                             , x + i, y + j))

    def _valid_ship_placement(self, ship_name, orientation, dimension, coordinate):
        """
        Method that checks if a ship placement is a valid one. Raises exceptions if not. Calls helper function to check
            for overlapping ships. Checks if a ship placement fits within the board dimensions.
        :param ship_name: name of ship to place (string)
        :param orientation: 'vertical' or 'horizontal'
        :param dimension: (m,n) dimensions of a ship to place (2-tuple of integers)
        :param coordinate: (x,y) coordinate of the TOP LEFT-MOST corner of the ship
        :return: does not return
        """
        self._check_ship_overlap(ship_name, orientation, dimension, coordinate)

        d0, d1 = dimension
        x, y = coordinate

        longer_d = max(d0, d1)
        shorter_d = min(d0, d1)

        if y > self.board_y - 1:
            raise ValueError(
                "y-coord of ship placement cannot be greater than %d. You entered %d." % (self.board_y - 1, y))
        if x > self.board_x - 1:
            raise ValueError(
                "x-coord of ship placement cannot be greater than %d. You entered %d." % (self.board_x - 1, x))

        # orient the ship such that its longest dimension is along the y-axis
        if orientation == 'vertical':
            if y + longer_d > self.board_y:
                raise ValueError("%s's y dimension of %d does not fit on board at the specified coordinate (%d,%d)"
                                 % (ship_name, longer_d, x, y))
            if x + shorter_d > self.board_x:
                raise ValueError("%s's x dimension of %d does not fit on board at the specified coordinate (%d,%d)"
                                 % (ship_name, shorter_d, x, y))
        # orient the ship such that its longest dimension is along the x-axis
        elif orientation == 'horizontal':
            if y + shorter_d > self.board_y:
                raise ValueError("%s's y dimension of %d does not fit on board at the specified coordinate (%d,%d)"
                                 % (ship_name, shorter_d, x, y))
            if x + longer_d > self.board_x:
                raise ValueError("%s's x dimension of %d does not fit on board at the specified coordinate (%d,%d)"
                                 % (ship_name, longer_d, x, y))
        else:
            raise ValueError("Orientation must be vertical or horizontal. You entered: %s" % orientation)

    def place_ship(self, ship_name, orientation, dimension, coordinate):
        """
        Method to place the ships on the boards. A ship is placed in such a way that the top left corner of the ship
        is at (x,y).
        vertical orientation means that the ship's longest dimension is along the y-axis and horizontal orientation
        means that the ships longest dimension is along the x-axis.
        :param ship_name: name of the ship being placed (string)
        :param orientation: 'vertical' or 'horizontal'
        :param dimension: (m,n) dimension of ship (2-tuple of integers)
        :param coordinate: (x,y) coordinate of the top left most coordinate of the ship
        :return: does not return
        """
        self._valid_ship_placement(ship_name, orientation, dimension, coordinate)
        d0, d1 = dimension
        x, y = coordinate
        longer_d = max(d0, d1)
        shorter_d = min(d0, d1)

        ship = Ship(ship_name, orientation, dimension)

        if orientation == 'vertical':
            for i in range(0, longer_d):
                for j in range(0, shorter_d):
                    self.my_board[(x + j, y + i)] = [ship, OCCUPIED]
                    ship.add_coordinates((x + j, y + i))
            self.life += d0 * d1
        elif orientation == 'horizontal':
            for i in range(0, longer_d):
                for j in range(0, shorter_d):
                    self.my_board[(x + i, y + j)] = [ship, OCCUPIED]
                    ship.add_coordinates((x + i, y + j))
            self.life += d0 * d1
        else:
            raise ValueError("Orientation must be vertical or horizontal. You entered: %s" % orientation)

    def get_tracking_board_as_list(self):
        """
        This method uses self.tracking_board to construct a simple nested list.
        :return: a list of lists containing the current state of the tracking board
        """
        l = list()
        for y in range(0, self.board_y):
            # s = '%d |' % y
            sub_l = list()
            for x in range(0, self.board_x):
                try:
                    sub_l.append(self.tracking_board[(x, y)])
                except KeyError:
                    sub_l.append(DEFAULT)
            l.append(sub_l)
        return l

    def get_my_ships_as_list(self):
        """
        This method uses self.my_board to construct a simple nested list.
        :return: a list of lists containing the current state of the board containing my fleet
        """
        l = list()
        for y in range(0, self.board_y):
            sub_l = list()
            for x in range(0, self.board_x):
                try:
                    sub_l.append(self.my_board[(x, y)][1])
                except KeyError:
                    sub_l.append(DEFAULT)
            l.append(sub_l)
        return l

    def _pretty_print(self, l):
        """
        Helper method for pretty printing
        :param l: list of lists that represent board states
        :return: does not return
        """
        x_label = '   x\t'
        g_line = 'y  '
        for i in range(0, self.board_x):
            x_label += '%d\t' % i
            g_line += '--------'

        print(x_label)
        print(g_line)

        for y in range(0, self.board_y):
            s = '%-2d |' % y
            for x in range(0, self.board_x):
                s += '\t%d' % l[y][x]
            print(s)

    def pretty_print_tracking_board(self):
        """
        Pretty print an ascii representation of the current state of the tracking board
        :return: does not return
        """
        print("%s's tracking board:" % self.name)
        l = self.get_tracking_board_as_list()
        self._pretty_print(l)

    def pretty_print_my_ships(self):
        """
        Pretty print an ascii representation of the current state of the board containing my fleet
        :return: does not return
        """
        print("%s's ships:" % self.name)
        l = self.get_my_ships_as_list()
        self._pretty_print(l)


# testing of player methods.
# use 'from game import *' instead to run the following lines of codes...
# if __name__ == "__main__":
#     p1= Player('John', (10, 10))
#     p2 = Player('Sam', (10, 10))
#     p1.place_ship("ship1", "vertical", (1, 5), (0, 0))
#     p1.place_ship("ship2", "vertical", (1, 1), (0, 9))
#     p1.place_ship("ship3", "vertical", (1, 1), (3, 9))
#     p1.place_ship("ship4", "horizontal", (2, 2), (8, 0))
#
#     p2.place_ship("ship1", "vertical", (1, 5), (1, 0))
#     p2.place_ship("ship2", "vertical", (1, 1), (0, 5))
#     p2.place_ship("ship3", "vertical", (1, 1), (9, 3))
#     p2.place_ship("ship4", "horizontal", (2, 2), (5, 0))
#
#     p1.shoot_and_update_boards(p2, (1, 0))
#     p2.shoot_and_update_boards(p1, (3, 0))
#
#     p1.shoot_and_update_boards(p2, (1, 1))
#     p2.shoot_and_update_boards(p1, (0, 3))
#
#     p1.shoot_and_update_boards(p2, (1, 2))
#     p2.shoot_and_update_boards(p1, (3, 9))
#
#     p1.shoot_and_update_boards(p2, (1, 3))
#     p2.shoot_and_update_boards(p1, (8, 0))
#
#     p1.shoot_and_update_boards(p2, (1, 4))
#     p2.shoot_and_update_boards(p1, (8, 1))
#
#     p1.shoot_and_update_boards(p2, (0, 5))
#     p2.shoot_and_update_boards(p1, (9, 0))
#
#     p1.shoot_and_update_boards(p2, (9, 3))
#     p2.shoot_and_update_boards(p1, (9, 1))
#
#     p1.shoot_and_update_boards(p2, (2, 2))
#     p2.shoot_and_update_boards(p1, (0, 0))
#
#     p1.shoot_and_update_boards(p2, (5, 0))
#     p2.shoot_and_update_boards(p1, (4, 1))
#
#     p1.shoot_and_update_boards(p2, (5, 1))
#     p2.shoot_and_update_boards(p1, (4, 2))
#
#     p1.shoot_and_update_boards(p2, (6, 0))
#     p2.shoot_and_update_boards(p1, (5, 5))
#
#     p1.shoot_and_update_boards(p2, (6, 1))
#     p2.shoot_and_update_boards(p1, (5, 6))
#
#     p1.pretty_print_tracking_board()
#     p1.pretty_print_my_ships()
#     p2.pretty_print_tracking_board()
#     p2.pretty_print_my_ships()
#
#     print p1.my_board[(0, 0)][0].coordinates
#     print p1.my_board[(8, 0)][0].coordinates
#
#     print("%s's life: %d" % (p1.name, p1.life))
#     print("%s dead: %s" % (p1.name, p1.is_dead()))
#     print("%s's life: %d" % (p2.name, p2.life))
#     print("%s dead: %s" % (p2.name, p2.is_dead()))
